"""
uropa.py: UROPA - Universal RObust Peak Annotator

@authors: Maria Kondili, Jens Preussner and Annika Fust
@license: MIT
@version: 2.0.1-alpha
@maintainer: Mario Looso
@email: mario.looso@mpi-bn.mpg.de
"""


import os
import sys
import json
import glob
import argparse
import logging
import datetime
import shutil
import subprocess as sp
import multiprocessing as mp
from itertools import chain
from functools import partial
from functools import reduce

import numpy as np

from . import config as cfg
from . import overlaps as ovls
from . import annotation as ant

#if __name__ == "__main__":
def main():
	parser = argparse.ArgumentParser(
		prog="uropa",
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
		"-p",
		"--prefix",
		dest="prefix",
		help="prefix for result file names (defaults to basename of input file)",
		required=False,
		action="store",
		metavar="prefix")
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
		"--add-comments",
		help="add comment lines to output files",
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
		version="%(prog)s 2.0.0-alpha")
	args = parser.parse_args()

	config = args.input

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
		if not os.path.exists(logpath) and logpath != '':
			try:
				os.makedirs(logpath)
			except OSError:
				logger.error("Could not create directory for log file {}".format(logpath))
		try:
			fileHandle = logging.FileHandler(args.log, mode='w')
			fileHandle.setLevel(logging.DEBUG)
			fileHandle.setFormatter(loggerFormat)
			logger.addHandler(fileHandle)
		except IOError:
			logger.error("Could not create log file {}".format(args.log))

	if args.prefix is not None:
		prefixpath = os.path.dirname(args.prefix)
		if not os.path.exists(prefixpath):
			if not prefixpath == '':
				try:
					os.makedirs(prefixpath)
				except IOError:
					logger.error("Could not create directory {} for output".format(prefixpath))
			else:
				prefixpath = '.'
		outdir = prefixpath + '/' + os.path.basename(args.prefix) + '_'
	else:
		outdir = "./" + os.path.splitext(os.path.basename(args.input))[0] + '_'

	logger.debug("Directory for output files is {}".format(outdir))
	logger.info("Start time: %s", datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))

	try:
		cfg_dict = cfg.parse_json(config)
	except IOError:
		logger.error("File %s does not exists or is not readable.", config)
		sys.exit()
	except ValueError as e:
		logger.error("File %s contains malformed JSON. %s", config, e)
		sys.exit()

	parameters = cfg.parse_parameters(cfg_dict, logger)
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

	gtf_feat = cfg.column_from_file(annot_gtf, 3, logger)
	
	print("gtf_feat = ", gtf_feat)

	if len(gtf_feat) < 1:
		logger.error("No features found in file {} for annotation.".format(annot_gtf))
		sys.exit()

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

	with open(outdir+"summary_config.json", "w") as fj:
		json.dump(summ_dict, fj, indent=4)

	distances = reduce(list.__add__, [q["distance"] for q in queries])
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

	#
	# Preparation of multiprocessing
	#
	spl_dir = outdir + "split_peaks/"
	if args.threads > 1:
		logger.info("Multiprocessing: Peak file will be split in %s smaller files.", args.threads)
		if not os.path.exists(spl_dir):
			os.makedirs(spl_dir)
		cmd = ['split',
			   '-n l/' + str(args.threads),
			   peaks_bed,
			   spl_dir + 'spl_peak_']

		try:
			sp.check_call(cmd, stderr=open(os.devnull, 'w'))
		except sp.CalledProcessError:
			args.threads = 1
			logger.warning(
				"Unable to split peak input into smaller files. Falling back to one thread.")
			logger.info("Check if split command is installed in version 8.22 or higher.")
		except OSError as e:
			args.threads = 1
			logger.warning(
				"Split command not available. Falling back to one thread.")

#
# Processing peaks
#
	input_args = [outdir, gtf_index, query_attributes, queries, max_distance, pr, gtf_has_chr]

	# > Write output according to Thread option
	if args.threads > 1:
		pool = mp.Pool(args.threads)
		partial_func = partial(ant.annotation_process, input_args)
		pool.map(partial_func, glob.glob(spl_dir + "spl_peak_*"))
		pool.close()
		pool.join()
	else:
		ant.annotation_process(input_args, peaks_bed, logger)
		# Files created after annot.process:

	allhits_partials = glob.glob(outdir + "allhits_part_*")
	finalhits_partials = glob.glob(outdir + "finalhits_part_*")

	logger.info("Writing output files to {}".format(outdir))

	if args.add_comments:
		comments = ovls.concat_comments(queries, str(pr), annot_gtf, peaks_bed)
	else:
		comments = None

	#
	# Merging output files
	#
	allhits_outfile = outdir + "allhits.txt"

	if len(queries) > 1 and not pr:
		besthits_outfile = outdir + "besthits.txt"
		merged_outfile = outdir + "finalhits.txt"

		besthits_partials = glob.glob(outdir + "besthits_part_*")
		ovls.finalize_file(merged_outfile, finalhits_partials, header, comments, log=logger)
		ovls.finalize_file(besthits_outfile, besthits_partials, header, comments, log=logger)
	else:
		besthits_outfile = outdir + "finalhits.txt"
		ovls.finalize_file(besthits_outfile, finalhits_partials, header, comments, log=logger)

	logger.debug("Filenames for output files are: {}, {}". format(allhits_outfile, besthits_outfile))

	ovls.finalize_file(allhits_outfile, allhits_partials, header, comments, log=logger)

	#
	# Reformat output
	#
	if args.reformat and len(queries) > 1 and not pr:
		logger.info("Reformatting output...")
		R_reform_Best = [
			'uropa_reformat_output.R',
			'-i',
			besthits_outfile,
			'-k',
			'peak_id',
			'-c',
			'1:5',
			'-d',
			',',
			'-t',
			str(args.threads)]
		try:
			# creates output of Best and gives name "Reformatted_"
			logger.debug('Reformat output call is {}'.format(R_reform_Best))
			pr_R = sp.check_output(R_reform_Best)
		except sp.CalledProcessError:
			logger.warning("Reformatted output could not be created with call %s", ' '.join(R_reform_Best))
		except OSError:
			logger.warning("Rscript command not available for summary output.")

	#
	# Visual summary
	#
	if args.summary:
		logger.info("Creating the Summary graphs of the results...")
		summary_script = "uropa_summary.R"
		summary_output = outdir + "summary.pdf"

		if len(queries) > 1 and not pr and os.path.exists(merged_outfile):
			call = [
				summary_script,
				"-f",
				merged_outfile,
				"-c",
				outdir + "summary_config.json",
				"-o",
				summary_output,
				"-b",
				besthits_outfile]
		else:
			call = [
				summary_script,
				"-f",
				besthits_outfile,
				"-c",
				outdir + "summary_config.json",
				"-o",
				summary_output]
		try:
			logger.debug('Summary output call is {}'.format(call))
			sum_pr = sp.check_output(call)
		except sp.CalledProcessError:
			logger.warning("Visualized summary output could not be created from %s.", ' '.join(call))
		except OSError:
			logger.warning("Rscript command not available for summary output.")

	#
	# Clean up of temporary files
	#
	outputs_ready = os.path.exists(
		allhits_outfile) and os.path.exists(besthits_outfile)

	if outputs_ready:
		#logger.debug("Attempting to clean {}".format(outdir))
		ovls.cleanup(outdir, logger)

		if os.path.exists(spl_dir):
			shutil.rmtree(spl_dir)
		if os.path.exists(outdir+"summary_config.json"):
			os.remove(outdir+"summary_config.json")
		os.remove(gtf_index)  # .gz
		os.remove(gtf_index + ".tbi")
		if len(gtf_feat) > 1:
			os.remove(gtf_cut_file)
			os.remove(gtf_cut_file + ".sorted")

	logger.info("End time: %s", datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
