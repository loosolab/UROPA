#!/usr/bin/env python
"""
uropa.py: UROPA - Universal RObust Peak Annotator

@authors: Maria Kondili, Jens Preussner and Annika Fust
@license: MIT
@version: 1.0
@maintainer: Mario Looso
@email: mario.looso@mpi-bn.mpg.de
"""

from __future__ import division
import os
import sys
import json
import glob
import argparse
import logging
import datetime
import subprocess as sp
import multiprocessing as mp
from itertools import chain
from functools import partial
from functools import reduce

import numpy as np

import uropa.config as cfg
import uropa.overlaps as ovls
import uropa.annotation as ant

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="uropa.py",
        description='UROPA - Universal RObust Peak Annotator.',
        epilog=cfg.howtoconfig(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-i",
        "--input",
        help="filename of configuration file",
        required=True,
        action="store",
        metavar="config.json")
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="directory for results and prefix of the output file name",
        required=False,
        action="store",
        metavar="uropa_out/",
        default="uropa_out/")
    parser.add_argument(
        "-r",
        "--reformat",
        help="create an additional compact and line-reduced table as result file",
        required=False,
        action="store_true")
    parser.add_argument(
        "-s",
        "--summary",
        help="filename of additional visualisation of results in graphical format",
        required=False,
        action="store_true")
    parser.add_argument(
        "-t",
        "--threads",
        help="multiprocessed run: n = number of threads to run annotation process",
        type=int,
        required=False,
        action="store",
        metavar="n",
        default=1)
    parser.add_argument(
        "--no-comments",
        help="do not show comment lines in output files",
        required=False,
        action="store_true")
    parser.add_argument(
        "-l",
        "--log",
        help="log file name for messages and warnings",
        action="store",
        metavar="uropa.log")
    parser.add_argument(
        "-d",
        "--debug",
        help="print verbose messages (for debugging) to stdout and log",
        required=False,
        action="store_true")
    parser.add_argument(
        "-v",
        "--version",
        help="prints the version and exits",
        action="version",
        version="%(prog)s 1.0")
    args = parser.parse_args()

    config = args.input
    outdir = args.output.strip("/") + "/"  # if '/' given ignored.

    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    streamHandle = logging.StreamHandler()
    loggerFormat = logging.Formatter('[%(levelname)s] - %(message)s')
    streamHandle.setFormatter(loggerFormat)

    if args.debug:
        streamHandle.setLevel(logging.DEBUG)
    else:
        streamHandle.setLevel(logging.WARNING)
    logger.addHandler(streamHandle)
    
    if args.log is not None:
	logpath = os.path.dirname(args.log)
        if not os.path.exists(logpath):
            try:
                os.makedirs(logpath)
                fileHandle = logging.FileHandler(args.log, mode='w')
                fileHandle.setLevel(logging.DEBUG)
                fileHandle.setFormatter(loggerFormat)
                logger.addHandler(fileHandle)
            except OSError:
                logger.error("Could not create directory for log file {}".format(logpath))
            except IOError:
                logger.error("Could not create log file {}".format(args.log))

    logger.info("Start time: %s", datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cfg_dict = cfg.parse_json(config)
    except IOError:
        logger.error("File %s does not exists or is not readable.", config)
        sys.exit()
    except ValueError as e:
        logger.error("File %s contains malformed JSON. %s", config, e)
        sys.exit()

    parameters = cfg.parse_parameters(cfg_dict, log=None)  # ,logger
    priority = parameters["priority"]
    annot_gtf = parameters["gtf"]
    peaks_bed = parameters["bed"]

    try:
        gtf_has_chr, gtf_cols = cfg.parse_first_gtf_line(annot_gtf)
    except IOError:
        logger.error("File %s does not exist or is not readable.", annot_gtf)
	sys.exit()

    # > Check GTF format
    if gtf_cols == 9:
        logger.info("GTF file format validated. Extracting all features from GTF now...")
    else:
        logger.warning("File %s is not a proper GTF file!", annot_gtf)

    gtf_feat = cfg.column_from_file(annot_gtf, 3)

    if not os.path.exists(peaks_bed):
        logger.error("File %s does not exists or is not readable.", peaks_bed)
        sys.exit()

    # Sanity check for other parameters
    accepted_val = ['T', 'True', 'TRUE', 'Yes', 'YES', 'Y', 'yes', 'F', 'False', 'FALSE', 'No', 'NO', 'N', 'no']
    if priority not in accepted_val:
        logger.error("Priority value should be one of the values from %s", accepted_val)
        sys.exit()

    # All parameters of Queries, filled-in with default values where necessary.
    all_queries = cfg.parse_queries(cfg_dict, gtf_feat, logger)
    logger.info("Number of all queries for parametric peak annotation: %s", len(all_queries))
    queries = cfg.remove_invalid_queries(all_queries, logger)
    logger.info("Number of valid queries for parametric peak annotation: %s", len(queries))

    # Validate query features
    query_features = list(chain.from_iterable([q["feature"] for q in queries]))
    feat_not_valid = [f for f in query_features if f not in gtf_feat]
    feat_valid = [f for f in query_features if f not in feat_not_valid]
    
    if feat_not_valid:
        logger.warning("Invalid features present (found in a query but not in the GTF): %s", ','.join(feat_not_valid))

    # > Cut gtf according to features of config, and index the cut.gtf for Faster Annotation
    # ! Attention : In the UCSC transformed gtf files,the feature is put by default "tfbs"
    if len(gtf_feat) > 1:
        gtf_cut_file = cfg.cut_gtf_perFeat(annot_gtf, feat_valid, outdir)
        mygtf = gtf_cut_file
    else:
        mygtf = annot_gtf

    # Create a new JSON for SUMMARY, with all keys completed :
    summ_dict = dict()
    summ_dict["queries"] = queries
    summ_dict["priority"] = priority
    summ_dict["gtf"] = annot_gtf
    summ_dict["bed"] = peaks_bed

    with open("summary_config.json", "w") as fj:
        json.dump(summ_dict, fj, indent=4)

    distances = reduce(list.__add__, map(lambda q: q["distance"], queries))
    max_distance = int(max(distances))

    logger.info("Distance for peak enlargment: %s", max_distance)

    gtf_index = mygtf + '.sorted.gz'

    if os.path.exists(gtf_index):
        logger.warning(
            "GTF-Index already existed before indexing. Will overwrite old index.")
    try:
        ovls.tabix_index(mygtf)  # Sort, zip, index the gtf
    except IOError:
        logger.error("Unable to create index for file %s. Make sure tabix, bgzip and sort are available and UROPA has rights to (over)write files.", mygtf)
        sys.exit()

    # Validate priority parameter
    pr = True if priority in ['T', 'True', 'TRUE', 'Yes', 'YES', 'Y', 'yes'] else False

    # Create list of Attributes from all queries together,to be shown in final
    # Table-columns for All queries
    query_attributes_none = list([q["show.attributes"] for q in queries])
    query_attributes = [a for a in np.unique(list(chain.from_iterable(query_attributes_none))) if a is not None and a != 'None']
    
    logger.info("Additional attributes included in output: %s", ','.join(query_attributes))
    
    # query included, when there is no hit from tabix
    nas_len = len(query_attributes) + 10
    NAsList = list(np.repeat("NA", nas_len))
    NAsList[nas_len - 1] = "- "

    header_comments = outdir + "cfg_header.txt"
    if not args.no_comments:
        ovls.write_header(header_comments, queries, str(pr), annot_gtf, peaks_bed)

    header_base = [
        "peak_id",
        "peak_chr",
        "peak_start",
        "peak_center",
        "peak_end",
        "feature",
        "feat_start",
        "feat_end",
        "feat_strand",
        "feat_anchor",
        "distance",
        "genomic_location",
        "feat_ovl_peak",
        "peak_ovl_feat"]
    
    header = "\t".join(header_base + query_attributes + ["query"])

    outdir_len = len(outdir.split("/"))
    outname = "" if outdir == "." else "_" + outdir.split("/")[outdir_len - 2]
    spl_dir = "splitted_peaks/"

    #
    # Preparation of multiprocessing
    #
    if args.threads > 1:
        logger.info("Multiprocessing: Peak file will be split in %s smaller files.", args.threads)
        if not os.path.exists(spl_dir):
            os.makedirs(spl_dir)
        cmd = ['split',
               '-n l/' + str(args.threads),
               '--additional-suffix=.bed',
               peaks_bed,
               spl_dir + 'spl_peak_']

        try:
            sp.check_call(cmd)
        except sp.CalledProcessError:
            args.threads = 1
            logger.warning(
                "Unable to split peak input into smaller files. Falling back to one thread.")
        except OSError as e:
            args.threads = 1
            logger.warning(
                "Split command not available. Falling back to one thread.")

#
# Processing peaks
#
    input_args = [outdir, gtf_index, query_attributes, queries, max_distance, pr, gtf_has_chr]

    # Output FileNames common for any thread option
    allhits_file = "AllHits" + outname + ".txt"
    allhits_outfile = outdir + "Uropa_" + allhits_file
    besthits_file = "BestHits" + outname + ".txt"
    besthits_outfile = outdir + "Uropa_" + besthits_file if len(
        queries) > 1 and not pr else outdir + "Uropa_FinalHits" + outname + ".txt"

    if len(queries) > 1 and not pr:
        merged_besthits_file = "Merged_BestHits" + outname + ".txt"
        merged_outfile = outdir + "Uropa_FinalHits" + outname + ".txt"

    # > Write output according to Thread option
    if args.threads > 1:
        if not os.path.exists(spl_dir):
            os.makedirs(spl_dir)

        pool = mp.Pool(args.threads)
        partial_func = partial(ant.annotation_process, input_args)
        pool.map(partial_func, glob.glob(spl_dir + "*.bed"))
        pool.close()
        pool.join()

        # Write out conc_files + header
        allhits_partials = glob.glob(outdir + "AllHits_Partial*")
        besthits_partials = glob.glob(outdir + "BestHits_Partial*")
    else:
        ant.annotation_process(input_args, peaks_bed, logger)
        # Files created after annot.process:
        allhits_partials = glob.glob(outdir + "AllHits_Partial*")
        besthits_partials = glob.glob(outdir + "BestHits_Partial*")

    
    ovls.write_final_file(
        args.threads,
        outdir,
        allhits_file,
        allhits_partials,
        allhits_outfile,
        header_comments,
        header,
        args.no_comments,
        logger)
    ovls.write_final_file(
        args.threads,
        outdir,
        besthits_file,
        besthits_partials,
        besthits_outfile,
        header_comments,
        header,
        args.no_comments,
        logger)

    if len(queries) > 1 and not pr:
        MergedBest_partials = glob.glob(
          outdir + "Merged_BestHits_Partial*")
        ovls.write_final_file(
            args.threads,
            outdir,
            merged_besthits_file,
            MergedBest_partials,
            merged_outfile,
            header_comments,
            header,
            args.no_comments,
            logger)

    outputs_ready = os.path.exists(
        allhits_outfile) and os.path.exists(besthits_outfile)
    # Delete partials after the concatenation
    if outputs_ready:
        del_tmp1 = ovls.delete_partials(
            "All", outdir, outname, spl_dir, args.threads)
        del_tmp2 = ovls.delete_partials(
            "Best", outdir, outname, spl_dir, args.threads)
        if del_tmp1 and del_tmp2:
            if len(queries) > 1 and not pr:
                del_tmp3 = ovls.delete_partials(
                    "Merged_Best", outdir, outname, spl_dir, args.threads)
                if del_tmp3:
                    if args.threads > 1:
                        ovls.del_spl_pks(spl_dir)

            elif len(queries) == 1 or pr:
                if args.threads > 1:
                    if del_tmp2:
                        ovls.del_spl_pks(spl_dir)
                else:
                    spl_dir = ""  # no splitting with t=1
                    del_tmp2 = ovls.delete_partials(
                        "Best", outdir, outname, spl_dir, args.threads)

    # Reformat All_hits if asked so :
    if args.reformat and len(queries) > 1 and not pr:
        logger.info("Reformatting output...")
        R_reform_Best = [
            'reformat_output.R',
            besthits_outfile,
            'peak_id',
            '1:5',
            ',']
        reformatBest_out = outdir + "Reformatted_" + \
            os.path.basename(besthits_outfile)
        try:
            # creates output of Best and gives name "Reformatted_"
            pr_R = sp.check_output(R_reform_Best)
        except sp.CalledProcessError:
            logger.warning("Reformatted output could not be created with call %s", ' '.join(R_reform_Best))
        except OSError:
            logger.warning("Rscript command not available for summary output.")

        # Add header and write to new file:
        reformatted_outfile = "Uropa_Reformatted_" + \
            os.path.basename(besthits_outfile)
        if os.path.exists(outdir + reformatBest_out):
            ovls.write_out_file(
                outdir +
                reformatted_outfile,
                reformatBest_out,
                header_comments,
                header)
        if os.path.exists(outdir + reformatted_outfile):
            logger.info("Reformatted BestHits output: %s", reformatted_outfile)
            os.remove(outdir + reformatBest_out)

    #> Create the Visualisation Summary Output
    if args.summary:
        logger.info("Creating the Summary graphs of the results...")
        summary_script = "summary.R"
        summary_output = outdir + "Uropa_Summary.pdf"

        if len(queries) > 1 and not pr and os.path.exists(merged_outfile):
            call = [
                summary_script,
                merged_outfile,
                "summary_config.json",
                summary_output,
                besthits_outfile]
        else:
            call = [
                "Rscript",
                summary_script,
                besthits_outfile,
                "summary_config.json",
                summary_output]
        try:
            sum_pr = sp.check_output(call)
        except sp.CalledProcessError:
            logger.warning("Visualized summary output could not be created from %s.", ' '.join(call))
        except OSError:
            logger.warning("Rscript command not available for summary output.")
        if os.path.exists(summary_output):
            os.remove("summary_config.json")

# Remove all other un-necessary files :
    if outputs_ready:
        os.remove(gtf_index)  # .gz
        os.remove(gtf_index + ".tbi")
        if not args.no_comments:
            os.remove(header_comments)
        if len(gtf_feat) > 1:
            os.remove(gtf_cut_file)
            os.remove(gtf_cut_file + ".sorted")

    logger.info("End time: %s", datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
