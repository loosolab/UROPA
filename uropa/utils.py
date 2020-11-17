"""Contains helper functions for UROPA """
import json
from textwrap import dedent
import ast
import numpy as np
import os
import sys
import re
import traceback
import logging
from logging import handlers
import multiprocessing as mp
import time
import datetime

class UROPALogger(logging.Logger):

	logger_levels = {
						0: logging.INFO,
						1: logging.DEBUG,		#debugging info
						2: logging.DEBUG - 5	#deeper debugging info
					}

	def __init__(self, debug_level=0, log_f=None, q=None):
		""" 
		debug_level: Logging level as identified in logger_levels
		log_f: path to output logfile (in addition to stdout)
		q: queue for handling logging via QueueHandler 
		"""

		self.debug_level = debug_level
		self.log_f = log_f
		self.q = q

		#Create logger
		logging.Logger.__init__(self, "UROPA")

		####### Setup custom levels #######
		#Create custom level for deeper debug messages
		deeper_level = UROPALogger.logger_levels[2]
		logging.addLevelName(deeper_level, "DEBUG2")
		setattr(self, 'debug2', lambda *args: self.log(deeper_level, *args))

		#Set level and format
		self.level = UROPALogger.logger_levels[debug_level]
		self.setLevel(self.level)
		self.formatter = logging.Formatter("%(asctime)s (%(process)d) [%(levelname)s]\t%(message)s", "%Y-%m-%d %H:%M:%S")

		########## Setup streaming #########
		#Log file stream
		if log_f != None:
			try:
				log = logging.FileHandler(log_f, "w")
				log.setLevel(self.level)
				log.setFormatter(self.formatter)
				self.addHandler(log)
			except:
				sys.exit("ERROR: Could not create logfile '{0}'. Please check that the given path exists.".format(log_f))

		#Stdout stream
		if self.q == None:
			con = logging.StreamHandler(sys.stdout)		#console output
			con.setLevel(self.level)
			con.setFormatter(self.formatter)
			self.addHandler(con)

		#Stdout handled by queue
		else:
			h = logging.handlers.QueueHandler(self.q)  	# Just the one handler needed
			self.handlers = []
			self.addHandler(h)

		#logger is ready for use

	def start_logger_queue(self):
		""" start process for listening and handling through the main logger queue """

		self.listener = mp.Process(target=self.main_logger_process)
		self.listener.start()

	def main_logger_process(self):
		""" This process runs in the main thread and handles the logging events """

		mainlogger = UROPALogger(self.debug_level, self.log_f)	#no queue, this logger is for collecting logging from the queue
		mainlogger.debug("Started main logger process")
		while True:
			try:
				record = self.q.get()
				if record is None:
					break
				mainlogger.handle(record) 	#this logger is running in the main process

			except EOFError:
				mainlogger.error("Logger lost connection to queue - probably due to an error raised from a child process.")
				break

		return(0)

	def stop_logger_queue(self):
		""" Stop process for listening """

		self.debug("Waiting for listener to finish")
		self.q.put(None)
		while self.listener.exitcode != 0:
			self.debug("Listener exitcode is: {0}. Waiting for exitcode = 0.".format(self.listener.exitcode))
			time.sleep(0.1)

		self.debug("Joining listener")
		self.listener.join()
	

#Validation of config
def howtoconfig():
    """Defines the epilog that is given when help is requested."""
    epilog = dedent("""\
    UROPA is a peak annotation tool facilitating the analysis of next-generation sequencing methods such
    as ChIPseq and ATACseq. The advantage of UROPA is that it can accommodate advanced structures of annotation
    requirements. UROPA is developed as an open source analysis pipeline for peaks generated from standard peak callers.

    Please cite upon usage:
    Kondili M, Fust A, Preussner J, Kuenne C, Braun T and Looso M. UROPA: A tool for Universal RObust Peak Annotation.
    Scientific Reports 7 (2017), doi: 10.1038/s41598-017-02464-y

    Please visit http://uropa-manual.readthedocs.io/config.html for detailed information on configuration.

    """)
    """
    More information on how to set up the config-file is found at:
    https://uropa-manual.readthedocs.io/config.html


    The configuration file should at least contain paths for bed and GTF files:

    {
    "queries": [],
    "bed": "/path/to/bed/file.bed",
    "gtf": "/path/to/annotation/file.gtf"
    }

    Different query types can be defined using the queries key:

    {
    "queries": [
      {...},
      {...}],
    "bed": "/path/to/bed/file.bed",
    "gtf": "/path/to/annotation/file.gtf"
    }

    Optionally, the priority key can be used to fine tune UROPAs behaviour:

    {
    "queries": [
      {...},
      {...}],
    "bed": "/path/to/bed/file.bed",
    "gtf": "/path/to/annotation/file.gtf",
    "priority": "True"
    }

    Please visit http://uropa-manual.readthedocs.io/config.html for detailed information on configuration.
	"""
    return epilog

def get_valid_filename(s):
	"""
	Return the given string converted to a string that can be used for a clean
	filename. Remove leading and trailing spaces; convert other spaces to
	underscores; and remove anything that is not an alphanumeric, dash, underscore, or dot.
	from django.utils.text
	"""
	s = str(s).strip().replace(' ', '_')
	return(re.sub(r'(?u)[^-\w.]', '', s))

def parse_json(infile):
    """ Read a json file to a dict """
    with open(infile) as f:
        return ast.literal_eval(json.dumps(json.load(f)))


def format_config(cfg_dict, logger):
	""" Format input config to catch any errors """
	
	query_prefix = "query_"
	case_conversion = {"peakinsidefeature": "PeakInsideFeature", "featureinsidepeak": "FeatureInsidePeak", 
						"upstream": "Upstream", "downstream":"Downstream", "overlapstart":"OverlapStart", "overlapend": "OverlapEnd"}
	convert_values = {value: True for value in [True, 't', 'true', 'yes', 'y']}
	convert_values.update({value: False for value in [False, 'f', 'false', 'no', 'n']})
	

	###################### Upper level config keys ####################
	#Check existance of upper-level keys
	valid_config_keys = set(["queries", "priority", "show_attributes", "gtf", "bed", "prefix", "outdir", "threads", "output_by_query"])
	given_config_keys = set(cfg_dict.keys())
	invalid_config_keys = given_config_keys - valid_config_keys
	if len(invalid_config_keys) > 0:
		logger.error("Error in config file: Key(s) {0} not known to UROPA.".format(invalid_config_keys))
		sys.exit()

	#Delete empty keys
	for key in list(cfg_dict.keys()):
		if is_empty(cfg_dict[key]):
			del cfg_dict[key]

	#Check format of values
	if "show_attributes" not in cfg_dict:
		cfg_dict["show_attributes"] = []
	else:
		if not isinstance(cfg_dict["show_attributes"], list):	#make sure that show_attributes is a list
			cfg_dict["show_attributes"] = [cfg_dict["show_attributes"]]

	#Convert all forms of true/false to python bool value
	cfg_dict["priority"] = convert_values[str(cfg_dict.get("priority", False)).lower()] 	#per default false
	cfg_dict["output_by_query"] =  convert_values[str(cfg_dict.get("output_by_query", False)).lower()]

	####################### Query level keys ##########################
	#Convert keys for backwards compatibility {old:new, (...)}
	conversion = {"show.attributes":"show_attributes", "feature.anchor": "feature_anchor", "filter.attribute":"filter_attribute", 
					"attribute.values": "attribute_values", "attribute.value": "attribute_values", "attribute_value": "attribute_values", 
					"direction": "relative_location"}
	valid_query_keys = set(["feature", "feature_anchor", "distance", "strand", "relative_location", "internals", "filter_attribute", "attribute_values", "name"])

	#Check and fill queries with needed defaults such as distance
	for i, query in enumerate(cfg_dict["queries"]):

		#Convert keys for backwards compatibility
		for key in list(query.keys()):
			if key in conversion:
				query[conversion[key]] = query[key]
				del query[key]

		#Move show_attributes to upper_level if given
		if "show_attributes" in query:
			if type(query["show_attributes"]) == list:
				for att in query["show_attributes"]:
					if att not in cfg_dict["show_attributes"]:
						cfg_dict["show_attributes"].append(att)
			else:
				if query["show_attributes"] not in cfg_dict["show_attributes"]:
					cfg_dict["show_attributes"].append(query["show_attributes"])
			del query["show_attributes"]
		
		#Check if there are attributes in query which are not in the "allowed" values
		query_keys = set(query.keys())
		invalid_keys = query_keys - valid_query_keys
		if len(invalid_keys) > 0:
			logger.error("Error in query {0}. Key(s) {1} are not known to UROPA.".format(i+1, invalid_keys))
			sys.exit()

		#Delete empty keys
		for key in list(query.keys()):
			if is_empty(query[key]):
				del query[key]

		# If filter_attribute is set, attribute_values has to be set as well
		if ("filter_attribute" in query and "attribute_values" not in query) or ("attribute_values" in query and "filter_attribute" not in query):
			logger.error("Error in query {0}. Keys for filter_attribute/attribute_values have to be set together.".format(i+1))
			sys.exit()

		##### Check content of individual keys #####
		if "distance" in query:
			try:
				if type(query["distance"]) == list:
					query["distance"] =  [int(query["distance"][0]), int(query["distance"][-1])]
				else:
					query["distance"] = [int(query["distance"]), int(query["distance"])]	#same distance in both positions
			except:
				logger.error("Error trying to convert distance \"{0}\" to integer - please check the format of this value.".format(query["distance"]))
				sys.exit()
		else:
			logger.error("No 'distance' not given in query: {0}".format(query))
			sys.exit()

		#Internals
		internalval = query.get("internals", False)
		query["internals"] = float(convert_values.get(str(internalval).lower(), internalval))	#if internals is a float, the value will not be converted
		if query["internals"] == 0:
			del query["internals"]

		#Keys which should be lists (sets) to search in 
		for key in ["feature", "feature_anchor", "attribute_values", "relative_location"]:
			if type(query.get(key, [])) != list:
				query[key] = set([query[key]])

		#Check the default values of input
		if "strand" in query:
			query["strand"] = query["strand"].lower()
			valid = set(['+', '-', 'same', 'opposite', 'ignore'])
			if query["strand"] not in valid:
				logger.error("Invalid strand ({0}) set in query {1}. Valid options are: {2}".format(query["strand"], i+1, valid))
				sys.exit()

		if "feature_anchor" in query:
			query["feature_anchor"] = set([element.lower() for element in query["feature_anchor"]])
			valid = set(["start", "center", "end"])
			invalid = query["feature_anchor"] - valid
			if len(invalid) > 0:
				logger.error("Invalid feature_anchor ({0}) set in query {1}. Valid options are: {2}".format(invalid, i+1, valid))
				sys.exit()

		if "relative_location" in query:
			query["relative_location"] = set([case_conversion.get(str(element).lower(), element) for element in query["relative_location"]])
			valid = set(["PeakInsideFeature", "FeatureInsidePeak", "Upstream", "Downstream", "OverlapStart", "OverlapEnd"])
			invalid = query["relative_location"] - valid
			if len(invalid) > 0:
				logger.error("Invalid relative_location ({0}) set in query {1}. Valid options are: {2}".format(invalid, i+1, valid))
				sys.exit()

		#Name the query if it was not already named
		if "name" not in query:
			query["name"] = query_prefix + str(i + 1)

	############## Warnings related to config/queries #############
	#Check for general input in queries, such as no show_attributes
	if len(cfg_dict.get("show_attributes", [])) == 0:
		logger.warning("No show_attributes given in config - no attributes for annotations are displayed in output.")

	#Catch duplicates in query names	
	query_names = [query["name"] for query in cfg_dict["queries"]]
	if len(query_names) != len(set(query_names)):
		logger.warning("Duplicated query names present: {0}".format(query_names))

	return(cfg_dict)



def config_string(cfg_dict):
	""" Pretty-print cfg_dict with one-line queries """

	upper_level = ["queries", "show_attributes", "priority",  "gtf", "bed", "prefix", "outdir", "threads", "output_by_query"]
	query_level = ["feature", "feature_anchor", "distance", "strand", "relative_location", "filter_attribute", "attribute_values", "internals", "name"]

	upper_lines = []
	for upper_key in upper_level:
		if upper_key == "queries":
			query_lines = "\"queries\":[\n"
			
			#Convert sets to lists
			for query in cfg_dict["queries"]:
				for key in query:
					if type(query[key]) == set:
						query[key] = list(query[key])

			query_strings = [json.dumps(query, sort_keys=True) for query in cfg_dict["queries"]]
			query_lines += "    " + ",\n    ".join(query_strings) + "\n          ]"

			upper_lines.append(query_lines)
		
		elif upper_key == "show_attributes" and upper_key in cfg_dict:
			upper_lines.append("\"{0}\": {1}".format(upper_key, json.dumps(cfg_dict[upper_key])))

		else:
			if upper_key in cfg_dict:
				upper_lines.append("\"{0}\": \"{1}\"".format(upper_key, cfg_dict[upper_key]))
		
	config_string = "{\n" + ",\n".join(upper_lines) + "\n}\n"

	return(config_string)

def check_file_access(fil, logger):
	""" Check if file exists and can be read """

	if os.path.isfile(fil):
		if not os.access(fil, os.R_OK):
			logger.error("File %s could not be read.", fil)
			sys.exit()
	else:
		logger.error("File %s does not exist.", fil)
		sys.exit()

def check_bed_format(bedfile, logger):
	""" Checks whether bedfile has the correct format """

	with open(bedfile) as f:
		for i, line in enumerate(f):
			if not re.match("(\S)+\s+([0-9]+)\s+([0-9]+)(\s+\S+)?(\s+[0-9,.]+)?(\s+[.\-+])?", line):
				logger.error("Line {0} in {1} is not proper bed format: {2}".format(i+1, bedfile, line))
				sys.exit()

	#todo: also check the number of columns in file

def parse_bedlines(bedlines, gtf_has_chr):
	""" Parse a list of bedlines to internal peaks format """

	peaks = [{}]*len(bedlines)	#initialize to length of bedlines; eliminates the need to append
	for i, line in enumerate(bedlines):
		columns = line.rstrip().split()

		#bed6-columns
		chrom, start, end = columns[0], int(columns[1]), int(columns[2])
		name = columns[3] if len(columns) > 3 else "peak_{0}".format(i+1) 
		score = columns[4] if len(columns) > 4 else "."
		strand = columns[5] if len(columns) > 5 else "."

		#Additional columns
		if len(columns) > 6:
			additional = columns[6:]
			additional_header = ["custom_" + str(val) for val in range(1,len(additional)+1)]
		else:
			additional_header = []
			additional = []

		#Key for the matching gtf chromosome
		if gtf_has_chr == True:
			gtf_chr = "chr" + chrom if not chrom.startswith("chr") else chrom		#add chr to match gtf if needed
		else:
			gtf_chr = chrom.replace("chr", "") #gtf chrom should not have chr-prefix
		
		peak_dict = {"gtf_chr": gtf_chr, "peak_chr":chrom, "peak_start":start, "peak_end":end, "peak_id":name, "peak_score":score, "peak_strand":strand}
		peak_dict.update(dict(zip(additional_header, additional)))
		peaks[i] = peak_dict

	return(peaks)


def check_chr(file, lines=100):
	"""Checks if a file has lines starting with 'chr'."""
    
	chrom = False
	count = 0
	with open(file, "r") as f:
		for line in f:
			if not line.startswith("#"):

				if line.startswith("chr"):
					chrom = True
					break

				count += 1	
				if count == lines:
					break

	return(chrom)

def subset_gtf(gtf, features, sub_gtf):
	"""Removes lines with features not in features from a gtf file."""
	feat2cut = set(np.unique(features))

	with open(gtf, "r") as f:
		lines = f.readlines()
		gtf_query_feat = [line for line in lines if not line.startswith("#") and line.split("\t")[2] in feat2cut]

	# List of lines containing only selected features from query
	with open(sub_gtf, "w") as f:
		f.write("".join(gtf_query_feat))	

def is_empty(value):
	""" Check whether value is empty """
	if (type(value) == str and value.strip() == "") or (type(value) == list and len(value) == 0):
		return(True)
	else:
		return(False)

def sorted_file_writer(q, file_dict, logger_options):
	""" Write strings in the correct order coming from Queue """

	#Start logger
	logger = UROPALogger(**logger_options)

	#Open handles for files
	file_handles = {}
	for key in file_dict:
		file = file_dict[key]
		try:
			file_handles[key] = open(file, "w")
		except Exception as e:
			print("Error opening file {0} in file_writer".format(file))
			print(e)
			return(0)

	#Fetching string content from queue
	idx_to_write = {key: 0 for key in file_dict}	#Start with idx == 0
	ready_to_write = {key:{} for key in file_dict}

	delta = datetime.timedelta(seconds=10) #Write debug status every 10 seconds
	prev_time = datetime.datetime.now()
	while True:

		#Write debug status
		current_time = datetime.datetime.now()
		if current_time - prev_time > delta: 
			n_ready_to_write = {key: sorted(list(ready_to_write[key].keys())) for key in ready_to_write}	#dict of idx-lists per key
			logger.debug("Writer task status | ready to write: {0}".format(n_ready_to_write))
			prev_time = current_time

		#Fetch annotated sites from queue
		try:
			(key, idx, content) = q.get() #idx is an integer starting at 0, content is a string

			if key == None:
				break	#no more content to write 
			
			#Add content to indexes ready to write
			ready_to_write[key][idx] = content

			#Write across keys
			for key in file_dict:
				while idx_to_write[key] in ready_to_write[key]:
					content = ready_to_write[key][idx_to_write[key]]
					file_handles[key].write(content)

					del ready_to_write[key][idx_to_write[key]] #Content has been written for this idx; free up memory!
					idx_to_write[key] += 1	#increment to write next block
					

		except Exception as e:
			logger.error('Error occurred during file writing: {0}'.format(type(e)))
			logger.debug("Full traceback: {0}".format(traceback.format_exc()))
			return(1)

	#Got all content in queue, close file
	for key in file_dict:
		file_handles[key].close()
	
	return(0)	