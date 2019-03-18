#!/usr/bin/env python3
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


def parse_json(infile):
    """ Read a json file to a dict """
    with open(infile, 'r', encoding='utf-8') as f:
        return ast.literal_eval(json.dumps(json.load(f)))


def format_config(cfg_dict):
	""" Format input config to catch any errors """
	
	convert_values = {value: True for value in [True, 'T', 'True', 'TRUE', 'Yes', 'YES', 'Y', 'yes']}
	convert_values.update({value: False for value in [False, 'F', 'False', 'FALSE', 'No', 'NO', 'N', 'no']})
	query_prefix = "query_"

	#Set upper-level keys
	cfg_dict["priority"] = convert_values[cfg_dict.get("priority", False)]

	for i, query in enumerate(cfg_dict["queries"]):

		#Feature
		if type(query.get("feature", [])) != list:
			query["feature"] = [query["feature"]]

		if type(query.get("feature_anchor", [])) != list:
			query["feature_anchor"] = [query["feature_anchor"]]

		if type(query.get("attribute_values", [])) != list:
			query["attribute_values"] = [query["attribute_values"]]

		#Internals
		internalval = query.get("internals", False)
		query["internals"] = float(convert_values.get(internalval, internalval))	#if internals is a float, the value will not be converted

		if "distance" in query:
			if type(query["distance"]) == list:
				query["distance"] =  [int(query["distance"][0]), int(query["distance"][1])]
			else:
				query["distance"] = [int(query["distance"]), int(query["distance"])]	#same distance in both positions

		#Name the query if it was not already named
		if "name" not in query:
			query["name"] = query_prefix + str(i + 1)

	return(cfg_dict)

def config_string(cfg_dict):
	""" Pretty-print cfg_dict with one-line queries """

	upper_level = ["queries", "show_attributes", "priority",  "gtf", "bed"]
	query_level = ["feature", "feature_anchor", "distance", "strand", "relative_location", "filter_attribute", "attribute_values", "internals", "name"]

	upper_lines = []
	for upper_key in upper_level:
		upper_str = "\"{0}\":".format(upper_key)

		if upper_key == "queries":
			
			queries = []
			for query in cfg_dict[upper_key]:

				one_query = []
				for query_key in query_level:
					query_string = ""

					if query_key in query:
						value = None
						if type(query[query_key]) == list:
							if len(query[query_key]) > 0:
								value = "[" + ",".join(["\"{0}\"".format(value) for value in query[query_key]]) + "]"
						else:
							if query[query_key] != None:
								value = "\"{0}\"".format(query[query_key])
						
						if value is not None:
							query_string += "\"{0}\": {1}".format(query_key, value)
							one_query.append(query_string)

				querystr = "    {" + ", ".join(one_query) + "}"
				queries.append(querystr)

			upper_str += "[\n" + ",\n".join(queries) + "\n]"

		elif upper_key == "show_attributes":
			upper_str  += "[" + ",".join(["\"{0}\"".format(value) for value in cfg_dict[upper_key]]) + "]"

		else:
			upper_str += "\"{0}\"".format(cfg_dict[upper_key])

		upper_lines.append(upper_str )

	fstr = "{\n" + ",\n".join(upper_lines) + "\n}\n"

	return(fstr)

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
				gtf_chr = "chr" + chrom if "chr" not in chrom else chrom

			peak_dict = {"gtf_chr": gtf_chr, "peak_chr":chrom, "peak_start":start, "peak_end":end, "peak_id":name, "peak_score":score, "strand":strand, "internal_peak_id": "peak_{0}".format(i+1)}
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
	feat2cut = np.unique(features)

	with open(gtf, "r") as f:
		lines = f.readlines()
		gtf_query_feat = [line for line in lines if line.startswith("#") or line.split("\t")[2] in feat2cut]

	# List of lines containing only selected features from query
	with open(sub_gtf, "w") as f:
		f.write("".join(gtf_query_feat))	


