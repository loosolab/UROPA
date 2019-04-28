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
import copy

import logging
import multiprocessing as mp
import pysam

#Import internal functions
from .utils import *
from .annotation import *
from .__init__ import __version__ as VERSION

def restricted_float(f, f_min, f_max):
    f = float(f)
    if f < f_min or f > f_max:
        raise argparse.ArgumentTypeError("{0} not in range [0.0, 1.0]".format(f))
    return f

def split_options(options):
	#Splits ","-separated options from commandline into lists
	return sum([opt.split(",") if type(opt) == str else [opt] for opt in options], [])


def main():

	############################################################################################################
	#################################################### INPUT #################################################
	############################################################################################################

	start_time = datetime.datetime.now()
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

	one_query.add_argument("--feature-anchor", help="Specific feature anchor to annotate to", metavar="", choices=["start", "center", "end"], nargs="*", default=[])
	one_query.add_argument("--distance", help="Maximum permitted distance from feature (1 or 2 arguments)", metavar="", nargs="*", type=int, default=[1000,10000])
	one_query.add_argument("--strand", metavar="", help="Desired strand of annotated feature relative to peak", choices=['ignore', 'same', 'opposite'], default='ignore')
	one_query.add_argument("--relative-location", metavar="", help="Peak location relative to feature location", nargs="*", choices=["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"], default=[])
	one_query.add_argument("--internals", metavar="", help="Set minimum overlap fraction for internal feature annotations. 0 equates to internals=False and 1 equates to internals=True. Default is False.", type=lambda x: restricted_float(x, 0, 1), default=False)
	one_query.add_argument("--filter-attribute", metavar="", help="Filter on 9th column of GTF", default="")
	one_query.add_argument("--attribute-values", help="Value(s) of attribute corresponding to --filter-attribute", nargs="*", metavar="", default=[])
	one_query.add_argument("--show-attributes", help="A list of attributes to show in output", metavar="", nargs="*", default=[])
	one_query.add_argument("--priority", help="argparse.SUPPRESS", action="store_true", default=False)

	#arguments for backwards compatibility using "-" instead of "_" in argument names
	one_query.add_argument("--relative_location", metavar="", help=argparse.SUPPRESS, nargs="*", choices=["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"], default=[])	#deprecated but left for backwards compatibility
	one_query.add_argument("--feature_anchor", help=argparse.SUPPRESS, metavar="", choices=["start", "center", "end"], nargs="*", default=[])
	one_query.add_argument("--filter_attribute", metavar="", help=argparse.SUPPRESS, default="")	#deprecated but left for backwards compatibility
	one_query.add_argument("--attribute_values", help=argparse.SUPPRESS, nargs="*", metavar="", default=[])
	one_query.add_argument("--show_attributes", help=argparse.SUPPRESS, metavar="", nargs="*", default=[])

	#Or configuration arguments for multiple queries (overwrites)
	multi_query = parser.add_argument_group("Multi-query configuration file")
	multi_query.add_argument("-i", "--input", help="Filename of configuration file (keys in this file overwrite command-line arguments about query)", action="store", metavar="config.json")

	#Other arguments
	additional = parser.add_argument_group("Additional arguments")
	additional.add_argument("-p", "--prefix", metavar="", help="Prefix for result file names (defaults to basename of .bed-file)")
	additional.add_argument("-o", "--outdir", metavar="", help="Output directory for output files (default: current dir)", default=".")
	#additional.add_argument("-r","--reformat", help="create an additional compact and line-reduced table as result file", action="store_true")
	additional.add_argument("--output-by-query", help="Additionally create output files for each named query seperately", action="store_true")
	additional.add_argument("-s","--summary", help="Create additional visualisation of results in graphical format", action="store_true")
	additional.add_argument("-t","--threads", help="Multiprocessed run: n = number of threads to run annotation process", type=int, action="store", metavar="n", default=1)
	additional.add_argument("-l","--log", help="Log file name for messages and warnings (default: log is written to stdout)", action="store", metavar="uropa.log")
	additional.add_argument("-d","--debug",help="Print verbose messages (for debugging)", action="store_true")
	additional.add_argument("-v","--version", help="Prints the version and exits", action="version", version="%(prog)s " + VERSION)
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
	cmd_query = {"feature":split_options(args.feature),
					 "feature_anchor":split_options(args.feature_anchor),
					 "distance": [args.distance[0], args.distance[0]] if len(args.distance) == 1 else args.distance,
					 "strand": args.strand,
					 "relative_location": split_options(args.relative_location),
					 "internals": args.internals,
					 "filter_attribute": args.filter_attribute,
					 "attribute_values": split_options(args.attribute_values),
					 }
	cmd_query["distance"] = split_options(cmd_query["distance"])

	valid_query_keys = set(list(cmd_query.keys()) + ["name"])

	#create cfg_dict like it would have been parsed from config .json
	cfg_dict = {"queries": [cmd_query],
				"show_attributes": split_options(args.show_attributes),
				"priority": args.priority,
				"gtf": args.gtf,
				"bed": args.bed,
				"prefix": args.prefix,
				"outdir": args.outdir,
				"threads": args.threads,
				"output_by_query": args.output_by_query
				}

	logger.debug("Config from command-line arguments: {0}".format(cfg_dict))

	#### Read from config file
	#Next, overwrite with config arguments if given, otherwise the arguments fall back to commandline default
	config = args.input
	if config != None:
		try:
			json_cfg_dict = parse_json(config)
			logger.debug("Config from json: {0}".format(json_cfg_dict))
			for key in json_cfg_dict:
				cfg_dict[key] = json_cfg_dict[key] 	#config values always win over commandline input
		except IOError:
			logger.error("File %s does not exists or is not readable.", config)
			sys.exit()
		except ValueError as e:
			logger.error("File %s contains malformed JSON. %s", config, e)
			sys.exit()

	#Set prefix if not set
	if cfg_dict["prefix"] == None:
		cfg_dict["prefix"] = os.path.splitext(os.path.basename(cfg_dict["bed"]))[0]	
	output_prefix = os.path.join(cfg_dict["outdir"], cfg_dict["prefix"])
	logger.debug("Output_prefix set to: {0}".format(output_prefix))		

	#Format keys in cfg_dict and exit if error
	cfg_dict = format_config(cfg_dict, logger)
	logger.debug("Formatted config: {0}".format(cfg_dict))

	#Write out formatted config file
	cfg_dict_filled = copy.deepcopy(cfg_dict)
	for query in cfg_dict_filled["queries"]:
		query["relative_location"] = query.get("relative_location", ["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"])
		query["strand"] = query.get("strand", 'ignore')
		query["feature_anchor"] = query.get("feature_anchor", ["start", "center", "end"])
	
	#----------------------------------------------------------------------------------------------------------#		
	# Validate existance of gtf / bed input and writability of output
	#----------------------------------------------------------------------------------------------------------#

	#Check if bed & gtf files exists
	for key in ["bed", "gtf"]:
		if cfg_dict[key] is not None:
			check_file_access(cfg_dict[key], logger)
		else:
			logger.error("No .{0}-file given as input - please check that a .{0}-file is given either via the commandline option --{0} or in the configuration file.".format(key))
			sys.exit()

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

	peaks = parse_bedfile(cfg_dict["bed"], gtf_has_chr)	#list of peak-dictionaries
	logger.debug("Read {0} peaks from {1}".format(len(peaks), cfg_dict["bed"]))

	#Establish order of peaks
	internal_peak_ids = [peak["internal_peak_id"] for peak in peaks]

	#----------------------------------------------------------------------------------------------------------#
	# Prepare GTF and extract chosen features to a subset gtf-file if needed
	#----------------------------------------------------------------------------------------------------------#		

	logger.info("Preparing .gtf-file for fast access")

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
	gtf_specific = list(set(gtf_feat) - set(query_feat)) 	#features in gtf which are not taken into account in queries
	if len(gtf_specific) > 0:
		sub_gtf = output_prefix + "_feature_subset.gtf"
		logger.debug("Subsetting {0} -> {1} with features {2}".format(cfg_dict["gtf"], sub_gtf, query_feat))
		subset_gtf(cfg_dict["gtf"], query_feat, sub_gtf)
		anno_gtf = sub_gtf
		temp_files.append(sub_gtf)
	else:
		anno_gtf = cfg_dict["gtf"]

	#Compress and index using gzip/tabix
	logger.debug("Tabix compress")
	anno_gtf_gz = output_prefix + ".gtf.gz"
	anno_gtf_index = anno_gtf_gz + ".tbi"

	success = 0
	sort_done = 0
	while success == 0:
		try:
			pysam.tabix_compress(anno_gtf, anno_gtf_gz, force=True)
			anno_gtf_gz = pysam.tabix_index(anno_gtf_gz, index=anno_gtf_index, seq_col=0, start_col=3, end_col=4, keep_original=True, force=True, meta_char='#')
			temp_files.extend([anno_gtf_gz, anno_gtf_index])
			success = 1
			if sort_done == 1:
				logger.info("Sorting and indexing was successful")

		except Exception as e:

			#Exit if we already tried to sort file once
			if sort_done == 1:
				logger.error("Could not index .gtf-file - please check whether the file has the correct 9-column format.")	
				sys.exit()
	
			#Read in and sort gtf file
			anno_gtf_sorted = output_prefix + "_sorted.gtf"
			temp_files.append(anno_gtf_sorted)
			sort_call = "grep -v \"^#\" {0} | sort -k1,1 -k4,4n > {1}".format(anno_gtf, anno_gtf_sorted)

			logger.warning("Indexing failed - the GTF is probably unsorted")
			logger.warning("Attempting to sort with call: {0}".format(sort_call))

			try:
				sub = subprocess.check_output(sort_call, shell=True)
			except subprocess.CalledProcessError:
				logger.error("Could not sort GTF file using command-line call: {0}".format(sort_call))
				sys.exit()

			anno_gtf = anno_gtf_sorted
			sort_done = 1

	#Write config used for annotation
	json_string = config_string(cfg_dict_filled)
	f = open(output_prefix + ".json", "w")
	f.write(json_string)
	f.close()

	############################################################################################################
	################################################## Annotation ##############################################
	############################################################################################################

	logger.info("Started annotation")
	threads = int(cfg_dict["threads"])
	
	#Split bed into chunks
	n_chunks = 100
	chunk_size = int(np.ceil(len(peaks)/float(n_chunks)))
	peak_chunks = [peaks[i:i+chunk_size] for i in range(0, len(peaks), chunk_size)]
	n_chunks = len(peak_chunks)

	if cfg_dict["threads"] > 1:

		pool = mp.Pool(threads)
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
		logger.info("Progress: {0:.0f}%".format(0/float(n_chunks)*100))
		for i, chunk in enumerate(peak_chunks):
			logger.debug("Chunk {0}".format(i+1))
			logger.debug("First peak: {0}".format(chunk[0]))
			logger.debug("Last peak: {0}".format(chunk[-1]))
			results.append(annotate_peaks(chunk, anno_gtf_gz, anno_gtf_index, cfg_dict, logger))
			logger.info("Progress: {0:.0f}%".format((i+1)/float(n_chunks)*100))

	#Join results from threads to one list
	all_annotations = sum(results, [])
	
	############################################################################################################
	################################################ POSTPROCESSING ############################################
	############################################################################################################

	logger.info("Processing annotated peaks")

	##### Check if no annotations were found #####
	all_NA = 0
	for anno in all_annotations:
		if "feature" in anno:
			all_NA = 1
	if all_NA == 0:	#This is 0 coming out of the loop if no features were found
		logger.warning("No annotations were found for input regions (all hits are NA). If this is unexpected, please check the configuration of your input queries.")
	
	#Add attribute columns to output
	logger.debug("Adding attribute columns")
	all_possible_attributes = {}
	for annotation in all_annotations:
		attributes_dict = annotation.get("feat_attributes", {})
		for key in attributes_dict:
			annotation["attribute_" + key] = attributes_dict[key]
			all_possible_attributes[key] = ""

	#Set output attribute columns
	attribute_columns = cfg_dict.get("show_attributes", [])
	
	#If "all" was set in show_attributes, set attributes_columns to total set of attributes
	if "all" in [str(att).lower() for att in attribute_columns]:
		attribute_columns = sorted(list(all_possible_attributes.keys()))
		logger.info("Config key show_attributes was set to \'all\'. All possible attributes are shown in output ({0})".format(attribute_columns))

	#Set output columns (the keys are different internally vs. the output columns)
	main = ["peak_chr", "peak_start", "peak_end", "peak_id", "peak_score", "peak_strand", "feature", "feat_start", "feat_end", "feat_strand", "feat_anchor", "distance", "relative_location", "feat_ovl_peak", "peak_ovl_feat"]
	header_internal = main + ["attribute_" + col for col in attribute_columns]  + ["query_name"]
	header_output = main + attribute_columns + ["name"]

	##### Write output files #####
	logger.info("Writing output files")

	#Make list of all hits in right order
	all_hits_sorted = sorted(all_annotations, key= lambda d: (d["internal_peak_id"], d.get("feat_start", 0)))	#use get because not all hits have feat_start

	header_str = "\t".join(header_output) + "\n"
	allhits_str = "\n".join(["\t".join([str(hit.get(key, "NA")) for key in header_internal]) for hit in all_hits_sorted]) + "\n"
	besthits_str = "\n".join(["\t".join([str(hit.get(key, "NA")) for key in header_internal]) for hit in all_hits_sorted if hit["best_hit"] == 1]) + "\n"

	#All hits
	logger.debug("Writing _allhits.txt")
	with open(os.path.join(output_prefix + "_allhits.txt"), "w") as f:
		f.write(header_str + allhits_str)
	with open(os.path.join(output_prefix + "_allhits.bed"), "w") as f:
		f.write(allhits_str)

	#Best hits
	logger.debug("Writing _besthits.txt")
	with open(os.path.join(output_prefix + "_finalhits.txt"), "w") as f:
		f.write(header_str + besthits_str)
	with open(os.path.join(output_prefix + "_finalhits.bed"), "w") as f:
		f.write(besthits_str)

	#Hits per query
	query_names = [query["name"] for query in cfg_dict["queries"]]	#the key is "name" in query line
	if cfg_dict["output_by_query"] == True:
		logger.info("Option --output-by-query is on. Writing additional hits-files per query.")
		for name in query_names:
			logger.debug("Writing hits for query: {0}".format(name))
			query_str = "\n".join(["\t".join([str(hit.get(key, "NA")) for key in header_internal]) for hit in all_hits_sorted if hit.get("query_name", "") == name]) + "\n"
			
			with open(os.path.join(output_prefix + "_" + get_valid_filename(name) + ".txt"), "w") as f:
				f.write(header_str + query_str)
			with open(os.path.join(output_prefix + "_" + get_valid_filename(name) + ".bed"), "w") as f:
				f.write(query_str)

	##### Visual summary #####
	if args.summary:
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
	if args.debug == False:
		logger.info("Cleaning up temporary files")
		for f in temp_files:
			try:
				os.remove(f)
			except:
				logger.warning("Could not remove temporary file {0}".format(f))

	end_time = datetime.datetime.now()
	total_time = end_time - start_time
	logger.info("UROPA run finished in {0}!".format(str(total_time).split('.', 2)[0]))
