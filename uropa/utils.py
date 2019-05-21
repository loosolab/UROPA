"""Contains helper functions for UROPA """

import json
from textwrap import dedent
import ast
import numpy as np
import os
import sys
import re

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
			valid = set(['ignore', 'same', 'opposite'])
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

def parse_bedfile(bedfile, gtf_has_chr):

	peaks = []
	with open(bedfile) as f:
		for i, line in enumerate(f):
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
			
			peak_dict = {"gtf_chr": gtf_chr, "peak_chr":chrom, "peak_start":start, "peak_end":end, "peak_id":name, "peak_score":score, "peak_strand":strand, "internal_peak_id": i+1}
			peak_dict.update(dict(zip(additional_header, additional)))
			peaks.append(peak_dict)

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