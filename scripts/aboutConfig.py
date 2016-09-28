#!/usr/bin/env python
import sys
import json
import os
import shlex
import subprocess
import logging
from subprocess import PIPE, Popen

def parse_json(infile):
	"""Read a json file"""
	assert isinstance(infile, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format('column',type(file),'str')
	
	try:
		with open(infile, 'r') as f:
			return json.load(f)
	except IOError as e:
		print("\nUnable to open file "+infile+"!\n\n")
		sys.exit()
	

def column_from_file(file, column):
	"""Extracts a given column from a file, and returns unified values as list."""
	assert isinstance(file, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format('column',type(file),'str')
	assert isinstance(column, int), 'Argument {0} of wrong type ({1}), should be {2}!'.format('column',type(column),'int')
	
	try:
		with open(file) as f:
			pass
	except IOError as e:
		print(e, "\nUnable to open file "+ file+ "!\n\n" )
		sys.exit()
	 
	cmd = 'cut -f'+str(column)+' '+str(file)+ ' | sort | uniq | grep -v "^#"'
	vals = subprocess.check_output(cmd, shell=True)
	return([v for v in vals.split('\n') if v !=""])

def find_unknown_keys(def_keys, cfg_keys):
	isunknown = map(lambda k :True if k in def_keys else k, cfg_keys)
	unknown_k = [v for i,v in enumerate(isunknown) if v !=True]
	if any(unknown_k):
		logging.info("\nWarning: Unknown key(s) {} given in config! Please make sure there are no typing errors.\n"
			    "For verifying the key names please check <uropa.sh -u>.\n"
			    "The given key will be ignored or replaced with default values if it is necessary for annotation.\n".format(unknown_k))
		if unknown_k == ["feature.position"] :
			logging.info("\nPlease replace the key feature.position with 'feature.anchor' and run UROPA again ! ")
			sys.exit()

	return
	

def parse_parameters(config):
	defaults = {"priority":"False", "bed": "no_peaks.bed", "gtf": "no_annotation.gtf"}  #, "bigwig": "none.bw"
	keys = defaults.keys()  
	values = map(lambda x: config[x] if x in config else defaults[x], keys)
	cfg_k  = config.keys() 
	
	#Check for invalid keys: 
	cfg_param =  [k for k in cfg_k if k !="queries"] # Keep basic keys of params, no "queries" (Careful: Value Error if queries not exist)
	find_unknown_keys(keys,cfg_param)
	parameters = dict(zip(keys, values))
	return(parameters)

def parse_queries(config, parameters, gtf_feat):

	defaults = {"feature": gtf_feat, "strand": ["+","-"], "show.attributes": "None", "filter.attribute": "None",
				"attribute.value":"None","distance": 100000, "feature.anchor": ["start","center","end"], 
				"direction": "any_direction" ,"internals" :"False"} 

	keys = defaults.keys() 

	try:
		query_list = config["queries"]
	except LookupError as e:
		logging.info("\nError: No query for annotation is defined in config!\n\n")
		sys.exit()

	if type(query_list) is list :
		pass
	else:
		query_list = [query_list]

	for q in query_list:
		find_unknown_keys(keys, q.keys())
		
	#def valid_features(query_list, gtf_feat) :
	cfg_features = [ q["feature"] for q in query_list  if "feature" in q ] #Only if feature:not empty
	#feat_exist = map(lambda f:f if  f not in gtf_feat, cfg_features)      #> [True, False,..]
	feat_not_valid = [f for f in  cfg_features  if  f not in gtf_feat ]    #> ['leopard']
	
	if any(feat_not_valid) :
		raise IOError ("Feature entered {} is not valid ! Possible values are: {} ".format(feat_not_valid, gtf_feat) )
		sys.exit()
		
	def give_val(q):
		return(map(lambda x: q[x] if x in q else defaults[x], keys))
	
	def make_list(l):
		return(map(lambda v: [v] if not isinstance(v, list) else v, l))
	
	vals = map(lambda l: give_val(l) ,query_list)
	values = map(lambda l: make_list(l), vals)
	queries = map(lambda x: dict(zip(keys, x)), values)
	return(queries)


def get_gtf_attribute(gtf, attribute):
	"""Extracts a given attribute from a gtf file, and returns unified values as list."""
	assert isinstance(gtf, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format('column',type(file),'str')
	assert isinstance(attribute, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format('column',type(column),'int')
	
	try:
		with open(gtf) as f:
			pass
	except IOError as e:
		print("\nUnable to open file "+gtf+"!\n\n")
		sys.exit()
	
	cmd = 'cut -f9 '+gtf+' | grep -v "^#" | awk \'BEGIN{FS="\t"}{n=split($1,a,"; ");for(i=1;i<=n;i++){split(a[i],b," ");if(b[1] == "'+attribute+'"){print b[2]}}}\' | tr -d \'"\' | sort | uniq'
	vals = subprocess.check_output(cmd, shell=True)
	return([v for v in vals.split('\n') if v !=""])


def get_gtf_line(gtf)	:
	"""Removes comment lines, reads first line to check for prefix chr- """
	import subprocess
	##> Check gtf opening: 
	try:
		with open(gtf) as f:
			pass
	except IOError as e:
		print("Unable to open file "+gtf+"!")

	with open(gtf, "r") as gtf_file:
		gtf_lines = gtf_file.readlines()
	comm_lines = len([li for li in gtf_lines if li.startswith("#")])  #5 for gencode, [] if no comm.lines
	gtf_line = gtf_lines[comm_lines]
	gtf_nocomm = gtf_lines[comm_lines:] # rest of lines after the No. comm_lines
	return(gtf_line,gtf_nocomm)


def cut_gtf_perFeat(annot_gtf, query_feats ) :	
	import  numpy as np
	import ntpath
	
	gtf_fname = ntpath.basename(annot_gtf)
	gtf_per_feat = gtf_fname.split(".gtf")[0]+"_cut_per_feat.gtf"
	feat2cut = np.unique( [qf for qf in query_feats ])

	gtf_line,gtf_nocomm = get_gtf_line(annot_gtf)
	gtf_has_chr = True if gtf_line.startswith('chr') else False
	
	gtf_query_feat = [li for li in gtf_nocomm if li.split("\t")[2] in feat2cut]

	#List of lines containing only selected features from query
	with open (gtf_per_feat , "w" ) as cutgtf :
		cutgtf.write("".join(gtf_query_feat))
		
	if os.path.exists(gtf_per_feat) :
		logging.info("\nNew shorter gtf with features of interest created successfully !")

	return(gtf_per_feat)