#!/usr/bin/env python3
# coding: utf-8
"""
uropa.py: UROPA - Universal RObust Peak Annotator

@authors: Annika Fust, Jens Preussner, Maria Kondili, Mette Bentsen and Mario Looso
@license: MIT
@maintainer: Mario Looso
@email: mario.looso@mpi-bn.mpg.de
"""


import os
import sys
import json
import argparse
import datetime
import time
import subprocess
import gzip

import logging
import multiprocessing as mp
import pysam
import pandas as pd

#Import internal functions
from uropa.utils import *
from uropa.annotation import *

def restricted_float(f, f_min, f_max):
    f = float(f)
    if f < f_min or f > f_max:
        raise argparse.ArgumentTypeError("{0} not in range [0.0, 1.0]".format(f))
    return f

def main():

	############################################################################################################
	#################################################### INPUT #################################################
	############################################################################################################

	cmd = " ".join(sys.argv)

	#----------------------------------------------------------------------------------------------------------#
	# Parse command-line arguments
	#----------------------------------------------------------------------------------------------------------#
	
	parser = argparse.ArgumentParser(
		prog="uropa",
		description='UROPA - Universal RObust Peak Annotator.',
		epilog=howtoconfig(),
		formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=35, width=90))
	
	#Configuation arguments for one query
	one_query = parser.add_argument_group("Arguments for one query")
	one_query.add_argument("-b", "--bed", metavar="", help="Filename of .bed-file to annotate", action="store")
	one_query.add_argument("-g", "--gtf", metavar="", help="Filename of .gtf-file with features", action="store")
	one_query.add_argument("--feature", help="Feature for annotation", metavar="", nargs="*", default=[])
	one_query.add_argument("--feature_anchor", help="Feature anchor to annotate to", metavar="", nargs="*", default=["start", "center", "end"])
	one_query.add_argument("--distance", help="Maximum permitted distance from feature (1 or 2 arguments)", metavar="", nargs="*", type=int, default=[1000,10000])
	one_query.add_argument("--strand", metavar="", help="Desired strand of annotated feature relative to peak", nargs="*", choices=['ignore', 'same', 'opposite'], default='ignore')
	one_query.add_argument("--relative_location", metavar="", help="Peak locaion relative to feature location", nargs="*", choices=["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"], default=["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"])
	one_query.add_argument("--internals", metavar="", help="Set minimum overlap fraction for internal feature annotations. 0 equates to internals=False and 1 equates to internals=True. Default is False.", type=lambda x: restricted_float(x, 0, 1), default=False)
	one_query.add_argument("--filter_attribute",metavar="", help="Filter on 9th column of GTF", default=None)
	one_query.add_argument("--attribute_values", help="Value(s) of attribute corresponding to --filter_attribute", nargs="*", metavar="", default=[])
	one_query.add_argument("--show_attributes", help="A list of attributes to show in output", metavar="", nargs="*", default=[])

	#Or configuration arguments for multiple queries (overwrites)
	multi_query = parser.add_argument_group("Multi-query configuration file")
	multi_query.add_argument("-i", "--input", help="Filename of configuration file (keys in this file overwrite command-line arguments about query)", action="store", metavar="config.json")

	#Other arguments
	additional = parser.add_argument_group("Additional arguments")
	additional.add_argument("-p", "--prefix", metavar="", help="Prefix for result file names (defaults to basename of .bed-file)")
	additional.add_argument("-o", "--outdir", metavar="", help="Output directory for output files (default: current dir)", default=".")
	#additional.add_argument("-r","--reformat", help="create an additional compact and line-reduced table as result file", action="store_true")
	additional.add_argument("-s","--summary", help="Filename of additional visualisation of results in graphical format", action="store_true")
	additional.add_argument("-t","--threads", help="Multiprocessed run: n = number of threads to run annotation process", type=int, action="store", metavar="n", default=1)
	#additional.add_argument("--add-comments",help="add comment lines to output files", action="store_true")
	additional.add_argument("-l","--log", help="Log file name for messages and warnings (default: log is written to stdout)", action="store", metavar="uropa.log")
	additional.add_argument("-d","--debug",help="Print verbose messages (for debugging)", action="store_true")
	additional.add_argument("-v","--version",help="Prints the version and exits", action="version",version="%(prog)s 3.0.1")
	args = parser.parse_args()

	#Write help if no input was given
	if len(sys.argv[1:]) == 0:
		parser.print_help()
		sys.exit()

	#Check valid input to deal with the split between command-line query and multi-query config file
	if args.input == None:
		if args.bed == None:
			sys.exit("ERROR: --bed is needed for annotation without --input")
		if args.gtf == None:
			sys.exit("ERROR: --gtf is needed for annotation without --input")


	#----------------------------------------------------------------------------------------------------------#
	# Configure logger
	#----------------------------------------------------------------------------------------------------------#

	logger = logging.getLogger(__name__)
	logger_format = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s', "%Y-%m-%d %H:%M:%S")
	logger_level = logging.DEBUG if args.debug else logging.INFO

	#Log vs. stream logger
	if args.log is not None:

		#Check if logfile can be created
		try:
			log = logging.FileHandler(args.log, "w")
			log.setLevel(logger_level)
			log.setFormatter(logger_format)
			logger.addHandler(log)
		except:
			sys.exit("ERROR: Could not create logfile {0}. Please check that the given path exists.".format(args.log))

	else:
		#Stdout stream
		stream = logging.StreamHandler(sys.stdout)	
		stream.setLevel(logger_level)
		stream.setFormatter(logger_format)
		logger.addHandler(stream)

	logger.setLevel(logger_level)
	

	############################################################################################################
	############################################ VALIDATION OF INPUT ###########################################
	############################################################################################################
	
	logger.info("Started UROPA")
	logger.info("Working directory: {0}".format(os.getcwd()))
	logger.info("Command-line call: {0}".format(cmd))
	temp_files = []

	# Validate output folder
	outdir = args.outdir
	if not os.path.exists(outdir):
		try:
			logger.debug("Creating directory {}".format(outdir))
			os.makedirs(outdir)
		except Exception as e:
			logger.error(e)
			logger.error("Could not create directory {} for output".format(outdir))

	#----------------------------------------------------------------------------------------------------------#
	# Establish queries from command-line and --input
	#----------------------------------------------------------------------------------------------------------#

	logger.info("Reading configuration from commandline/input config")

	#First, fill in parameters from commandline
	default_query = {"feature":args.feature,
					 "feature_anchor":args.feature_anchor,
					 "distance": [args.distance[0], args.distance[0]] if len(args.distance) == 1 else args.distance,
					 "strand": args.strand,
					 "relative_location": args.relative_location,
					 "internals": args.internals,
					 "filter_attribute": args.filter_attribute,
					 "attribute_values": args.attribute_values,
					 }

	#create cfg_dict like it would have been parsed from config .json
	cfg_dict = {"queries": [default_query],
				"show_attributes": args.show_attributes,
				"priority": False,
				"gtf": args.gtf,
				"bed": args.bed
				}

	logger.debug("Config from command-line arguments: {0}".format(cfg_dict))

	#Next, overwrite with config arguments if given, otherwise the arguments fall back to commandline default
	config = args.input
	if config != None:
		try:
			json_cfg_dict = parse_json(config)
			logger.debug("Config from json: {0}".format(json_cfg_dict))
			for key in json_cfg_dict:
				cfg_dict[key] = json_cfg_dict[key] 	#config values always win over commandline
		except IOError:
			logger.error("File %s does not exists or is not readable.", config)
			sys.exit()
		except ValueError as e:
			logger.error("File %s contains malformed JSON. %s", config, e)
			sys.exit()

	#Fill each key with defaults if they were not set
	for query in cfg_dict["queries"]:
		for key in default_query:
			query[key] = query.get(key, default_query[key])

	#Format keys in cfg_dict
	cfg_dict = format_config(cfg_dict)
	logger.debug("Formatted config: {0}".format(cfg_dict))

	#Check for general input in queries, such as no show_attributes
	if len(cfg_dict["show_attributes"]) == 0:
		logger.warning("No show_attributes given - no attributes for annotations are displayed in output.")

	#catch duplicates in query names	
	query_names = [query["name"] for query in cfg_dict["queries"]]
	if len(query_names) != len(set(query_names)):
		logger.warning("Duplicates in query names: {0}".format(query_names))

	#----------------------------------------------------------------------------------------------------------#		
	# Validate gtf / bed input
	#----------------------------------------------------------------------------------------------------------#

	#Check if bed & gtf files exists
	check_file_access(cfg_dict["bed"], logger)
	check_file_access(cfg_dict["gtf"], logger)

	#Check prefix
	if args.prefix == None:
		args.prefix = os.path.splitext(os.path.basename(cfg_dict["bed"]))[0]	

	output_prefix = os.path.join(args.outdir, args.prefix)
	logger.debug("Output_prefix set to: {0}".format(output_prefix))

	#Check whether output files can be written
	output_files = [os.path.join(output_prefix + suffix) for suffix in ["_allhits.txt", "_allhits.bed", "_finalhits.txt", "_finalhits.bed"]]
	for f in output_files:
		if os.path.exists(f) and not os.access(f, os.W_OK):
			logger.error("Output file {0} is not writable.".format(f))
			sys.exit()


	############################################################################################################
	################################################## PREPARATION #############################################
	############################################################################################################
	
	#----------------------------------------------------------------------------------------------------------#
	# Prepare bed for internal region-structure
	#----------------------------------------------------------------------------------------------------------#				
	
	logger.info("Reading .bed-file to annotate")

	#Check bed format and parse to internal structure
	check_bed_format(cfg_dict["bed"], logger)
	gtf_has_chr = check_chr(cfg_dict["gtf"])	#True/False

	peaks = parse_bedfile(cfg_dict["bed"], gtf_has_chr)	
	logger.debug("Read {0} peaks from {1}".format(len(peaks), cfg_dict["bed"]))

	#Establish order of peaks
	internal_peak_ids = [peak["internal_peak_id"] for peak in peaks]

	#Split bed into chunks
	n_chunks = 100
	peak_chunks = [peaks[i::n_chunks] for i in range(n_chunks)]


	#----------------------------------------------------------------------------------------------------------#
	# Prepare GTF and extract chosen features to a subset gtf-file if needed
	#----------------------------------------------------------------------------------------------------------#		

	logger.info("Preparing .gtf for fast access")

	#Check all possible features in gtf
	logger.debug("Finding all possible features in gtf")
	gtf_feat_count = {}
	with open(cfg_dict["gtf"]) as f:
		for line in f:
			if not line.startswith("#"):
				columns = line.rstrip().split("\t")
				
				if len(columns) < 9:
					logger.error("Input GTF ({0}) has less than 9 columns - please check that the file has the correct GTF format.".format(cfg_dict["gtf"]))
					sys.exit()

				feature = columns[2]

				if feature not in gtf_feat_count:
					gtf_feat_count[feature] = 0
				gtf_feat_count[feature] += 1
	gtf_feat = list(gtf_feat_count.keys())
	logger.debug("Features in gtf: {0}".format(gtf_feat_count))

	#Fill in empty feature keys with all possible 
	for query in cfg_dict["queries"]:
		if len(query.get("feature", [])) == 0:
			query["feature"] = gtf_feat

	#Count all features given in config
	query_feat = []
	for query in cfg_dict["queries"]:
		query_feat.extend(query["feature"])
	query_feat = list(set(query_feat))

	#Check if any features were given that are not possible to subset on
	not_in_gtf = list(set(query_feat) - set(gtf_feat))
	if len(not_in_gtf) > 0:
		logger.error("Query feature(s) {0} not found in gtf".format(not_in_gtf))
		sys.exit()

	#Subset gtf if needed
	logger.debug("Subsetting gtf if needed")
	gtf_specific = list(set(gtf_feat) - set(query_feat)) 	#features specific for gtf but which are not taken into account in queries
	if len(gtf_specific) > 0:
		sub_gtf = output_prefix + "_feature_subset.gtf"
		logger.debug("Subsetting {0} -> {1} with features {2}".format(cfg_dict["gtf"], sub_gtf, query_feat))
		subset_gtf(cfg_dict["gtf"], gtf_feat, sub_gtf)
		anno_gtf = sub_gtf
		temp_files.append(sub_gtf)
	else:
		anno_gtf = cfg_dict["gtf"]

	#Compress and index using gzip/tabix
	logger.debug("Tabix compress")
	anno_gtf_gz = output_prefix + ".gtf.gz"
	anno_gtf_index = anno_gtf_gz + ".tbi"
	pysam.tabix_compress(anno_gtf, anno_gtf_gz, force=True)
	anno_gtf_gz = pysam.tabix_index(anno_gtf_gz, index=anno_gtf_index, seq_col=0, start_col=3, end_col=4, keep_original=True, force=True)
	temp_files.extend([anno_gtf_gz, anno_gtf_index])

	#Write out formatted config file
	json_string = config_string(cfg_dict)
	f = open(output_prefix + ".json", "w")
	f.write(json_string)
	f.close()

	############################################################################################################
	################################################## Annotation ##############################################
	############################################################################################################

	logger.info("Started annotation")
	n_chunks = len(peak_chunks)
	if args.threads > 1:

		pool = mp.Pool(args.threads)
		task_list = [pool.apply_async(annotate_peaks, args=(chunk, anno_gtf_gz, anno_gtf_index, cfg_dict, )) for chunk in peak_chunks]
		pool.close() 	#done sending jobs to pool

		#Wait for tasks to finish
		count = -1
		finished = sum([task.ready() for task in task_list])
		while finished < n_chunks:
			finished = sum([task.ready() for task in task_list])
			if count != finished:
				logger.info("Progress: {0:.0f}%".format(finished/float(n_chunks)*100))
				count = finished
			else:
				time.sleep(0.5)
		pool.join()

		#Get results from processes
		results = [task.get() for task in task_list]
		
	else:
		results = []
		for i, chunk in enumerate(peak_chunks):
			results.append(annotate_peaks(chunk, anno_gtf_gz, anno_gtf_index, cfg_dict, logger))
			logger.info("Progress: {0:.0f}%".format((i+1)/float(n_chunks)*100))

	#Join results from threads to one dictionary
	all_annotations = sum(results, [])
	

	############################################################################################################
	################################################ POSTPROCESSING ############################################
	############################################################################################################

	logger.info("Processing annotated peaks")

	#Add attribute columns
	#The keys are different internally vs. the output columns
	attribute_columns = cfg_dict["show_attributes"]
	main = ["peak_chr", "peak_start", "peak_end", "peak_id", "feature", "feat_start", "feat_end", "feat_strand", "feat_anchor", "distance", "relative_location", "feat_ovl_peak", "peak_ovl_feat"]
	header_internal = main + ["show_" + col for col in attribute_columns]  + ["query_name"]
	header_output = main + attribute_columns + ["name"]

	for annotation in all_annotations:
		attributes_dict = annotation["feat_attributes"]
		if type(attributes_dict) == dict:
			annotation.update({"show_" + key: attributes_dict[key] for key in attributes_dict})

	##### Write output files #####
	all_hits = pd.DataFrame(all_annotations)
	
	#Sort on peak_ids
	all_hits["original_order"] = [internal_peak_ids.index(peak_id) for peak_id in all_hits["internal_peak_id"]] #map position
	all_hits.sort_values(by=["original_order", "feat_start", "feat_end"])

	#All hits
	logger.debug("Writing _allhits.txt")
	all_hits.to_csv(os.path.join(output_prefix + "_allhits.txt"), na_rep="NA", sep="\t", index=False, columns=header_internal, header=header_output)
	all_hits.to_csv(os.path.join(output_prefix + "_allhits.bed"), na_rep="NA", sep="\t", index=False, columns=header_internal, header=False)

	#Best hits
	best_hits = all_hits.loc[all_hits["best_hit"] == 1]
	best_hits.to_csv(os.path.join(output_prefix + "_finalhits.txt"), na_rep="NA", sep="\t", index=False, columns=header_internal, header=header_output)
	best_hits.to_csv(os.path.join(output_prefix + "_finalhits.bed"), na_rep="NA", sep="\t", index=False, columns=header_internal, header=False)

	##### Visual summary #####
	logger.info("Creating the Summary graphs of the results...")
	summary_script = "uropa_summary.R"
	summary_output = output_prefix + "_summary.pdf"

	#cmd is the command-line call str
	call = [summary_script, "-f", os.path.join(output_prefix + "_finalhits.txt"), "-c", output_prefix + ".json", "-o", summary_output, "-b", os.path.join(output_prefix + "_allhits.txt"), "-a \'", cmd, "\'"]
	call_str = ' '.join(call)
	
	try:
		logger.debug('Summary output call is {}'.format(call_str))
		sum_pr = subprocess.check_output(call_str, shell=True)
	except subprocess.CalledProcessError:
		logger.warning("Visualized summary output could not be created from: %s", call_str)
	except OSError:
		logger.warning("Rscript command not available for summary output.")

	##### Cleanup #####
	logger.info("Cleaning up temporary files.")
	if args.debug == False:
		for f in temp_files:
			try:
				os.remove(f)
			except:
				logger.warning("Could not remove temporary file {0}".format(f))

	logger.info("UROPA run ended successfully!")
