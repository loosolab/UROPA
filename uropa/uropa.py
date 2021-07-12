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
import psutil
import traceback

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

def update_status(status_dict, task_list):
	""" Update status_dict with the information from task_list status """
	
	current_done = sum([task.ready() for task in task_list])
	status_dict["n_jobs_running"] = len(task_list) - current_done
	status_dict["n_jobs_done"] = status_dict["task_list_i"] + current_done #task_list_i is the previously finished jobs

	#Memory used
	status_dict["memory_percent"] = psutil.virtual_memory().percent

	return(status_dict)


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
	one_query.add_argument("--strand", metavar="", help="Desired strand of annotated feature relative to peak", choices=['+', '-', 'same', 'opposite', 'ignore'], default='ignore')
	one_query.add_argument("--relative-location", metavar="", help="Peak location relative to feature location", nargs="*", choices=["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"], default=[])
	one_query.add_argument("--internals", metavar="", help="Set minimum overlap fraction for internal feature annotations. 0 equates to internals=False and 1 equates to internals=True. Default is False.", type=lambda x: restricted_float(x, 0, 1), default=False)
	one_query.add_argument("--filter-attribute", metavar="", help="Filter on 9th column of GTF", default="")
	one_query.add_argument("--attribute-values", help="Value(s) of attribute corresponding to --filter-attribute", nargs="*", metavar="", default=[])
	one_query.add_argument("--show-attributes", help="A list of attributes to show in output (default: all)", metavar="", nargs="*", default=["all"])
	one_query.add_argument("--priority", help=argparse.SUPPRESS, action="store_true", default=False)

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
	additional.add_argument("-d","--debug",help="Print verbose messages (for debugging)", action="count", default=0)
	additional.add_argument("-v","--version", help="Prints the version and exits", action="version", version="%(prog)s " + VERSION)
	additional.add_argument("-c", "--chunk", metavar="", help="Number of lines per chunk for multiprocessing (default: 1000)", type=int, default=1000) 
	additional.add_argument("--target-mem", type=float, help=argparse.SUPPRESS, default=80)	#goal is to stay at maximum 80% memory consumption
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

	logger_q = mp.Manager().Queue()	#queue for multiprocessing logging
	logger = UROPALogger(debug_level=args.debug, log_f=args.log, q=logger_q) #debug_level is number of times --debug is given on commandline
	logger.start_logger_queue()	 #start listening for logging sent to queue
	logger_options = {"q": logger_q, "debug_level": args.debug}

	############################################################################################################
	############################################ VALIDATION OF INPUT ###########################################
	############################################################################################################
	
	logger.info("Started UROPA " + VERSION)
	logger.info("Working directory: {0}".format(os.getcwd()))
	logger.info("Command-line call: {0}".format(cmd))
	temp_files = []

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

			#Overwrite any values if given in config file
			for key in json_cfg_dict:
				cfg_dict[key] = json_cfg_dict[key] 	#config values always win over commandline input
			
			#Format and check values within json
			cfg_dict = format_config(cfg_dict, logger)

		except IOError:
			logger.error("File %s does not exists or is not readable.", config)
			sys.exit()
		except ValueError as e:
			logger.error("File %s contains malformed JSON. %s", config, e)
			sys.exit()

	# Validate output folder
	outdir = cfg_dict["outdir"]
	if not os.path.exists(outdir):
		try:
			logger.debug("Creating directory {}".format(outdir))
			os.makedirs(outdir)
		except Exception as e:
			logger.error(e)
			logger.error("Could not create directory {} for output".format(outdir))

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
	# Prepare GTF and extract chosen features to a subset gtf-file if needed
	#----------------------------------------------------------------------------------------------------------#		

	logger.info("Preparing .gtf-file for fast access")

	gtf_has_chr = check_chr(cfg_dict["gtf"])	#True/False

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

	#Find all possible attributes in gtf
	logger.debug("Finding all possible attributes in gtf")
	gtf_attribute_count = {}
	with open(cfg_dict["gtf"]) as f:
		for line in f:
			if not line.startswith("#"):
				columns = line.rstrip().split("\t")
			
				pairs = columns[8].split(";")
				attributes = [pair.lstrip().rstrip().split(" ")[0] for pair in pairs]
				for att in attributes:
					gtf_attribute_count[att] = 0
	logger.debug("gtf attributes: {0}".format(list(gtf_attribute_count.keys())))

	if "all" in [str(att).lower() for att in cfg_dict.get("show_attributes", [])]:
		show_attributes = sorted(list(gtf_attribute_count.keys()))
		show_attributes = [att for att in show_attributes if att != ""]
		logger.info("Config key show_attributes was set to \'all\'. All possible attributes are shown in output ({0})".format(show_attributes))
	else:
		show_attributes = cfg_dict.get("show_attributes", [])

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
	prev_time = datetime.datetime.now()

	#Checking bed file format
	check_bed_format(cfg_dict["bed"], logger)

	#Setup pool for async annotation of peak chunks
	threads = int(cfg_dict["threads"])
	pool = mp.Pool(processes=threads, maxtasksperchild=100)
	task_list = []
	max_jobs_running = threads - 1
	chunk_size = args.chunk
	chunk_i = 0

	#Establish files to write
	file_dict = {key: os.path.join(output_prefix + "_" + key) for key in ["allhits.bed", "allhits.txt", "finalhits.bed", "finalhits.txt"]}

	#Additional files if output_by_query == True
	if cfg_dict["output_by_query"] == True:
		logger.info("Option --output-by-query is on. Writing additional hits-files per query.")
		query_names = [query["name"] for query in cfg_dict["queries"]]
		for name in query_names:
			file_dict[name + ".bed"] = os.path.join(output_prefix + "_" + get_valid_filename(name) + ".bed")
			file_dict[name + ".txt"] = os.path.join(output_prefix + "_" + get_valid_filename(name) + ".txt")
	
	logger.debug("File dictionary: {0}".format(file_dict))

	#Start queue for writing output
	manager = mp.Manager()
	q = manager.Queue()
	writer_task = pool.apply_async(sorted_file_writer, args=(q, file_dict, logger_options))

	##Initialize files with header line (or nothing)
	main = ["peak_chr", "peak_start", "peak_end", "peak_id", "peak_score", "peak_strand", "feature", "feat_start", "feat_end", "feat_strand", "feat_anchor", "distance", "relative_location", "feat_ovl_peak", "peak_ovl_feat"]
	header_output = main + show_attributes + ["name"]
	header_str = "\t".join(header_output) + "\n"
	for key in file_dict:
		if key.endswith(".txt"):
			q.put((key, 0, header_str))
		else:
			q.put((key, 0, ""))

	#Dict for collecting information on jobs, memory etc. during run
	status_dict = {"n_jobs_done": 0, 
				   "max_jobs_running": threads - 1, 
				   "n_jobs_running": 0,
				   "task_list_i": 0}

	#Go through bedfile and annotate chunks
	peaks_read = 0
	end_of_file = 0
	delta = datetime.timedelta(seconds=5)
	task_list_i = 0 #number of finished tasks
	with open(cfg_dict["bed"]) as f:

		while end_of_file == 0:

			#Get chunk of lines
			chunk_lines = [f.readline() for _ in range(chunk_size)]
			chunk_lines = [line for line in chunk_lines if line != ""]
			n_lines = len(chunk_lines)
			if n_lines == 0:
				break	#last chunk is empty; break out of while loop and don't annotate

			chunk_i += 1
	
			logger.debug("Read {0} lines from chunk {1} (({2}) - ({3}))".format(n_lines, chunk_i, " ".join(chunk_lines[0].split()[:3]), " ".join(chunk_lines[-1].split()[:3])))
			if n_lines < chunk_size:
				end_of_file = 1 #End of the file has been reached

			#Create peaks format for chunk
			peaks = parse_bedlines(chunk_lines, gtf_has_chr, line_start=peaks_read) #outputs list of peak-dictionaries
			peaks_read += len(peaks) #update peaks_read count for next chunk
				
			if threads > 1:

				#Keep looping until job for this chunk has been started
				chunk_job_started = 0	
				while chunk_job_started == 0:

					#Check if writer is still runnning
					if writer_task.ready():
						logger.error("Writing of output files from multiprocessing jobs failed - please check any previous warnings.")
						sys.exit()

					#Update status dict
					status_dict = update_status(status_dict, task_list)

					#Write out progress after certain amount of time
					current_time = datetime.datetime.now()
					if current_time - prev_time > delta: 
						logger.info("Progress: Annotated {0} peaks ({1} jobs running; {2} jobs finished)".format(status_dict["n_jobs_done"] * chunk_size, 
																														     status_dict["n_jobs_running"], 
																														     status_dict["n_jobs_done"]))
						logger.debug("Max jobs allowed: {0}; Virtual memory percent: {1}; Writer task running: {2}; Writer queue size: {3}; logger queue size: {4}".format(status_dict["max_jobs_running"], 
																																											status_dict["memory_percent"], 
																																											not writer_task.ready(), 
																																											q.qsize(),
																																											logger_q.qsize()))
						logger.debug("Tasks in cache: {0}".format(list(pool._cache.keys())))
						prev_time = current_time

					#Test memory consumption and adjust max_jobs_running accordingly
					if status_dict["memory_percent"] == 100:
						logger.warning("Memory usage has reached 100% - this might cause UROPA to halt or crash. Reducing '--chunk' or '--threads' can help to resolve this issue.")	

					#How many jobs should be running to fulfill --target-mem consumption?
					memory_per_job = status_dict["memory_percent"] / max(1, status_dict["n_jobs_running"])
					status_dict["max_jobs_running"] = min(threads - 1, int(np.floor(args.target_mem / memory_per_job))) #maximum possible is threads - 1, but can be lower if memory becomes low
					status_dict["max_jobs_running"] = max(max_jobs_running, 1) # minimum 1 job running

					#### Check whether new jobs can be send to pool ###
					if status_dict["n_jobs_running"] >= status_dict["max_jobs_running"]:
						time.sleep(0.5) #wait half a second, and continue while-loop (if condition is True)

					else:
						#Add new chunk to pool
						logger.debug("Adding job for chunk {0}".format(chunk_i))
						task_list.append(pool.apply_async(annotate_peaks, args=(peaks, anno_gtf_gz, anno_gtf_index, cfg_dict, q, chunk_i, show_attributes, logger_options)))
						chunk_job_started = 1

					#Check exit status of any finished tasks
					for i, task in enumerate(task_list):
						if task.ready():
							try:
								task.get() #either successful or exited with exception
							except Exception as e:
								logger.error("Multiprocessing task exited with error: {0}".format(type(e)))
								logger.error("Please check previous warnings for resolving the issue.")
								logger.error("Full traceback:\n{0}".format(traceback.format_exc()))
								sys.exit(1)

					#If the first task in task_list was finished, it can be removed to reduce size of task_list
					while len(task_list) > 0 and task_list[0].ready():
						del task_list[0]
						status_dict["task_list_i"] += 1

			else:
				logger.debug("Annotating peak chunk")
				annotate_peaks(peaks, anno_gtf_gz, anno_gtf_index, cfg_dict, q, chunk_i, show_attributes, logger_options)

	# Whole file has been read and all jobs were added to task_list
	# Wait for all jobs to finish
	logger.info("The input .bed-file has been read and all jobs have been started. Waiting for the final tasks to finish...")
	while sum([task.ready() for task in task_list]) < len(task_list):
		logger.debug("Tasks in cache: {0}".format(list(pool._cache.keys())))
		time.sleep(0.5) 

	#Check results for final tasks
	for task in task_list:
		try:
			task.get() #either successful or exited with exception
		except Exception as e:
			logger.error("Multiprocessing task exited with error: {0}".format(type(e)))
			logger.error("Please check previous warnings for resolving the issue.")
			logger.debug("Full traceback:\n{0}".format(traceback.format_exc()))
			sys.exit(1)

	#End writer queue
	q.put((None, None, None))

	#Check that all queues are done writing
	while q.qsize() != 0:
		logger.debug("- Queue size {0}".format(q.qsize()))
		time.sleep(0.5) 

	writer_result = writer_task.get()	#locks until writer_task returns value (i.e. files were closed)

	pool.terminate()
	pool.join()

	############################################################################################################
	################################################ POSTPROCESSING ############################################
	############################################################################################################

	logger.info("Processing annotated peaks")

	"""
	##### Check if no annotations were found #####
	all_NA = 0
	for anno in all_annotations:
		if "feature" in anno:
			all_NA = 1
	if all_NA == 0:	#This is 0 coming out of the loop if no features were found
		logger.warning("No annotations were found for input regions (all hits are NA). If this is unexpected, please check the configuration of your input queries.")
	"""

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

	logger.stop_logger_queue()	#done logging
