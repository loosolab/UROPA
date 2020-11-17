"""Contains code for the annotation process"""

import pysam
from functools import reduce
import re
import numpy as np
import logging
import datetime

from .utils import * #import Uropa logging functions

def decimal_round(num, d=3):

	stringnum = "{:.20f}".format(num)

	#Position of first non-zero integer after decimal
	decimal_i = stringnum.index(".")
	nonzero_i_lst = [i for i in range(decimal_i+1, len(stringnum)) if int(stringnum[i]) > 0] + [0]	#If all describing digits are 0 (e.g. 0.0 or 1.0), nonzero_is is [0]
	nonzero_i = nonzero_i_lst[0]

	#Decide how to round
	if nonzero_i < decimal_i + d:	#If a non-zero integer was already found
		rounded = str(round(num, d))

	elif nonzero_i >= decimal_i + d: #If a non-zero integer was already found
		rounded = stringnum[:nonzero_i+1]

	return(rounded)

def create_anno_dict(peak, hit):
	""" Returns a dictionary containing information on the hit from gtf """

	#Add peak information
	anno_dict = {}
	anno_dict.update(peak) #fills out peak chr/start/end/id/score/strand
	anno_dict["peak_center"] = int((anno_dict["peak_end"] + anno_dict["peak_start"])/2.0)
	anno_dict["peak_length"] = anno_dict["peak_end"] - anno_dict["peak_start"]

	#Parse info from gtf string
	try:
		att = hit.attributes.strip("; ")	#remove trailing ;
		pairs = re.split(";\s*", att) 		#regex split on ;(space)

		pairs = [pair.split() for pair in pairs]
		attribute_tags = [pair[0] for pair in pairs]
		attribute_values = [" ".join(pair[1:]).replace("\"", "") for pair in pairs]
		
		#Join values from identical tags to list
		attribute_dict = {tag:[] for tag in attribute_tags}
		for i, (tag, value) in enumerate(zip(attribute_tags, attribute_values)):
			attribute_dict[tag].append(value)

	except Exception as e:
		print("Error reading attributes: {0} ({1})".format(hit.attributes, e))
		attribute_dict = {}

	# Fill in with feature info
	anno_dict["feature"] = hit.feature
	anno_dict["feat_strand"] = hit.strand
	anno_dict["feat_start"] = int(hit.start)
	anno_dict["feat_end"] = int(hit.end)
	anno_dict["feat_center"] = int((anno_dict["feat_end"] + anno_dict["feat_start"])/2.0)
	anno_dict["feat_length"] =  int(anno_dict["feat_end"] - anno_dict["feat_start"])
	anno_dict["feat_attributes"] = attribute_dict	# Dictionary of lists containig values {"key1":[value1], "key2":[val1,val2]} 

	#Look-up keys for annotation
	anno_dict["anchor_pos"] = {"start": anno_dict["feat_start"] if anno_dict["feat_strand"] != "-" else anno_dict["feat_end"],
								"center": anno_dict["feat_center"], 
								"end": anno_dict["feat_end"] if anno_dict["feat_strand"] != "-" else anno_dict["feat_start"]}

	#Change with each query
	anno_dict["query"] = 0	 #query for which the hit was valid
	anno_dict["best_hit"] = 0

	return(anno_dict)



def distance_to_peak_center(anno_dict, query_anchor):
    """ Assigns the distance of peak center to best query anchor """

    anchor_list = list(query_anchor)

    #Set default if anchor list is empty
    if len(query_anchor) == 0:
    	anchor_list = ["start", "center", "end"]

    #Calculate distances to each possible anchor
    raw_distances = [anno_dict["peak_center"] - anno_dict["anchor_pos"][anchor] for anchor in anchor_list]
    abs_distances = [abs(dist) for dist in raw_distances]
    min_dist_i = abs_distances.index(min(abs_distances))

    #Set minimum distance as best anchor
    anno_dict["raw_distance"] = raw_distances[min_dist_i]
    anno_dict["distance"] = int(abs(raw_distances[min_dist_i]))
    anno_dict["feat_anchor"] = anchor_list[min_dist_i]

    return(anno_dict)


# import "division" allows decimals
def calculate_overlap(anno_dict):
    """ Calculates percentage of length covered by the peak/feature """
    
    #beds exclude first position, therefore +1 for starts. Range excludes last position in range - therefore +1 for end
    ovl_range = range(max(anno_dict["peak_start"]+1, anno_dict["feat_start"]+1), min(anno_dict["peak_end"], anno_dict["feat_end"])+1)
    ovl_bp = len(ovl_range)

    ovl_pk = ovl_bp / float(anno_dict["peak_length"])
    ovl_feat = ovl_bp / float(anno_dict["feat_length"])

    anno_dict["feat_ovl_peak"] = decimal_round(ovl_pk, 3)    #Percentage of the peak that is covered by the feature (1.0 corresponds to the genomic_location “PeakInsideFeature”). 
    anno_dict["peak_ovl_feat"] = decimal_round(ovl_feat, 3)	 #Percentage of the feature that is covered by the peak (1.0 corresponds to the genomic_location “FeatureInsidePeak”).

    return(anno_dict)


def get_relative_location(anno_dict):
	""" Sets the relative location of peak to feature """

	location = "NA"
	if float(anno_dict["feat_ovl_peak"]) == 1:
		location = "PeakInsideFeature"

	elif float(anno_dict["peak_ovl_feat"]) == 1:
		location = "FeatureInsidePeak"

	elif float(anno_dict["feat_ovl_peak"]) == 0: #no overlap
		
		#If feature (gene) is on the - strand
		if anno_dict["feat_strand"] == "-":
			
			#Check if peak is upstream/downstream of anchor
			if anno_dict["peak_center"] > anno_dict["anchor_pos"][anno_dict["feat_anchor"]]:
				location = "Upstream" #For feature strand '-': If peak_center is higher than the anchor, the peak is upstream
			else:
				location = "Downstream"

		#Else, feature must be on the plus strand
		else:
			#Check if peak is upstream/downstream of anchor
			if anno_dict["peak_center"] > anno_dict["anchor_pos"][anno_dict["feat_anchor"]]:
				location = "Downstream" #For feature strand '+': If peak_center is higher than the anchor, the peak is downstream
			else:
				location = "Upstream"
	
	else:	#some overlap, but not completely internal

		#Figure out if it is overlapstart or overlap end
		if anno_dict["anchor_pos"]["start"] in range(anno_dict["peak_start"]+1, anno_dict["peak_end"]+1):
			location = "OverlapStart"

		elif anno_dict["anchor_pos"]["end"] in range(anno_dict["peak_start"]+1, anno_dict["peak_end"]+1):
			location = "OverlapEnd"

	anno_dict["relative_location"] = location

	return(anno_dict)


def annotate_single_peak(peak, tabix_obj, cfg_dict, logger=None):
	""" 
	Annotates a single peak against tabix_obj (GTF) using the configuration in queries

	Input:
		peak (dict): A dictionary containing information on peak. It has the form: {"peak_chr":"chr1", "peak_start":0, "peak_end":100, "peak_id":"peak1", "peak_score":0.4, "peak_strand":"+"}
					 This dict can also include gtf_chr in case the gtf has a different chromosome prefix, e.g.: { (...), "gtf_chr":1}
					 It might also contain other information such as: { (...), "additional_bed_column_1":"column_value"}
		tabix_obj (Pysam TabixFile): tabix_obj is an open pysam.TabixFile
		cfg_dict (dict): Configuration dictionary containing "queries" and "priority" keys
		logger (python.logging obj): Logger object for debugging or None

	Returns:
		valid_annotations (list): A list of dictionaries containing the full peak dictionary filled in with additional keys related to the annotated element. 
								  If no hits were found, the peak is returned without annotation information.
	"""

	#General info on queries
	queries = cfg_dict["queries"]
	n_queries = len(queries)
	distances = sum([query["distance"] for query in queries], [])
	max_distance = int(max(distances))

	#Annotation
	logger.debug2("Annotating peak: {0}".format(peak))

	valid_annotations = []	#for this peak
	stop_searching = False
	query_i = -1
	while query_i+1 < n_queries and stop_searching == False:

		query_i += 1				#First query is 0
		query = queries[query_i]	#current query to check

		logger.debug2("Finding hits for query: {0}".format(query))

		#Extend and fetch possible hits from tabix
		max_distance = max(query["distance"])
		extend_start = int(max(1, peak["peak_start"] - max_distance))
		extend_end = peak["peak_end"] + max_distance
		tabix_query = "{0}:{1}-{2}".format(peak.get("gtf_chr", peak["peak_chr"]), extend_start, extend_end)
		logger.debug2("Tabix query for query {0} ({1}): {2}".format(query_i, query["name"], tabix_query))

		try:
			begin = datetime.datetime.now()
			hits = list(tabix_obj.fetch(tabix_query, parser=pysam.asGTF()))	#hits for this query
			end = datetime.datetime.now()
			logger.debug2("Fetched {0} hits in {1}".format(len(hits), end - begin))
		except: 
			#exception if no hits could be fetched from tabix, for example if the contig does not exist in the gtf index.
			#print("ERROR: Could not create iterator for peak: {0} \n with tabix query {1}".format(peak, tabix_query))		
			stop_searching = True 
			hits = []

		begin = datetime.datetime.now()
		for hit in hits: 
			
			#If feature is not the right one, we do not have to go further - saves computation of distances
			if "feature" in query:
				if hit.feature not in query["feature"]:
					#logger.debug("{0} not in {1} - continuing to next hit".format(hit.feature, query["feature"]))
					continue

			anno_dict = create_anno_dict(peak, hit)
			anno_dict["query"] = query_i
			anno_dict["query_name"] = query["name"]

			#Calculate distances/relative location
			anno_dict = distance_to_peak_center(anno_dict, query.get("feature_anchor", []))
			anno_dict = calculate_overlap(anno_dict)
			anno_dict = get_relative_location(anno_dict)

			##### Test validity of the hit to query_i ####
			checks = {}
			#if "feature" in query:
			#	checks["feature"] = anno_dict["feature"] in query["feature"]	 #feature

			#Check feature anchor
			if "feature_anchor" in query:
				checks["feature_anchor"] = anno_dict["feat_anchor"] in query["feature_anchor"]

			#Peak strand relative to feature strand
			if "strand" in query:
				if query["strand"] != "ignore" and anno_dict["peak_strand"] != ".":
					checks["strand"] = ((anno_dict["peak_strand"] == query["strand"]) or
										(anno_dict["peak_strand"] == anno_dict["feat_strand"] and query["strand"] == "same") or 
										(anno_dict["peak_strand"] != anno_dict["feat_strand"] and query["strand"] == "opposite"))	

			#Check whether distance was valid
			if anno_dict["feat_strand"] == "+":
				checks["distance"] = anno_dict["raw_distance"] > -query["distance"][0] and anno_dict["raw_distance"] < query["distance"][1]
			else:
				checks["distance"] = anno_dict["raw_distance"] > -query["distance"][1] and anno_dict["raw_distance"] < query["distance"][0]

			#Check distance (Distance can still be valid if PeakInsideFeature/FeatureInsidePeak and internals flag is set)
			if "internals" in query:
				max_overlap = max(float(anno_dict["feat_ovl_peak"]), float(anno_dict["peak_ovl_feat"]))
				checks["distance"] = checks["distance"] or (query["internals"]*1.0 > 0 and max_overlap >= query["internals"]*1.0)	#if internals is set to more than 0 overlap

			#Filter on relative location
			if "relative_location" in query:
				checks["relative_location"] = anno_dict["relative_location"] in query["relative_location"]
			
			#Filter on attribute if any was set
			if "filter_attribute" in query and "attribute_values" in query: #query["filter_attribute"] != None:

				#Check if the desired filter attribute is in the attributes of the hit:
				checks["attribute"] = False
				if query["filter_attribute"] in anno_dict["feat_attributes"]:
					for filter_value in query["attribute_values"]:
						tag_values_list = anno_dict["feat_attributes"][query["filter_attribute"]]	#list of values for this tag
						if filter_value in tag_values_list:
							checks["attribute"] = True
			
			##### All checks are done -> establish if hit is a valid annotation #####
			valid = sum(checks.values()) == len(checks.values()) #all checks must be valid
			if valid:
				valid_annotations.append(anno_dict.copy())
			logger.debug2("Validity: {0} | Checks: {1} | Annotation dict: {2}".format(valid, checks, {key:anno_dict[key] for key in anno_dict}))
		
		end = datetime.datetime.now()
		logger.debug2("Validated hits in {0}".format(end-begin))

		#All tabix hits for this query were checked - if priority, stop searching if any valid hit was found -> else, check next query
		stop_searching = (len(valid_annotations) > 0 and cfg_dict["priority"]) or stop_searching #or if stop_searching was already set previously

		if stop_searching == True:
			logger.debug2("{0} valid hit(s) were found for query_i = {1} and priority is true - stopping search.".format(len(valid_annotations), query_i))
		else:
			logger.debug2("A total of {0} valid hits were found. Incrementing query_i.".format(len(valid_annotations), query_i))
	
	logger.debug2("")	#create empty line in debugger output for easy overview

	#After all hits have been checked for peak; make final checks and set best flag
	if len(valid_annotations) > 0:	

		#Sort valid annotations
		valid_annotations = sorted(valid_annotations, key= lambda anno_dict: (anno_dict["feat_start"], anno_dict["feat_end"], anno_dict["feature"]))
		
		#If priority == True, find the highest ranked annotations for this peak
		#if cfg_dict["priority"] == True:
		#	highest_priority_query = min([anno_dict["query"] for anno_dict in valid_annotations])
		#	#logger.debug("Highest priority hit for {0} was {1}".format(peak, highest_priority_query))
		#	valid_annotations = [anno_dict for anno_dict in valid_annotations if anno_dict["query"] == highest_priority_query]

		distances = [anno_dict["distance"] for anno_dict in valid_annotations]
		best_hit_index = distances.index(min(distances))
		valid_annotations[best_hit_index]["best_hit"] = 1

	else:
		valid_annotations = [peak]
		valid_annotations[0]["best_hit"] = 1			#the empty hit for the peak is the best hit

	return(valid_annotations)


def annopeak_to_string(annotated_peak, columns=None, attributes=[]):
	""" Format an annotated peak to a .bed-file output """

	#Default output
	if columns == None:
		columns = ["peak_chr", "peak_start", "peak_end", "peak_id", "peak_score", "peak_strand"]
		columns += ["feature", "feat_start", "feat_end", "feat_strand", "feat_anchor", "distance", "relative_location", "feat_ovl_peak", "peak_ovl_feat"]

	#Fetch columns from peak in the correct order
	annotation_columns = [str(annotated_peak.get(key, "NA")) for key in columns]
	attribute_columns = [",".join(annotated_peak.get("feat_attributes", {}).get(key, ["NA"])) for key in attributes]

	bed_str = "\t".join(annotation_columns + attribute_columns + [annotated_peak.get("query_name", "NA")])

	return(bed_str)


def annotate_peaks(peaks, gtf_gz, gtf_index, cfg_dict, q, idx, attributes, logger_options):
	""" 
		Input: 
		peaks (list): List of dictionaries containing information on peaks to annotate (see function 'annotate_single_peak')
		gtf_gz (str): Path to gtf.gz file
		gtf_index (str): Path to gtf.gz index 
		cfg-dict (dict): The loaded config containing queries
		q (Queue): The queue to put annotations into
		idx (int): The order in which the annotations should be written to output
		attributes (list): A list of attribute columns to write to output,
		logger_options (dict): A dict for initializing UROPALogger
	"""

	logger = UROPALogger(**logger_options)

	#Open tabix file
	tabix_obj = pysam.TabixFile(gtf_gz, index=gtf_index)

	#For each peak in input peaks, collect all_valid_annotations
	logger.debug("Annotating peaks in chunk {0}".format(idx))
	all_valid_annotations = []
	for peak in peaks:
		
		#Annotate single peak
		valid_annotations = annotate_single_peak(peak, tabix_obj, cfg_dict, logger=logger)
		all_valid_annotations.extend(valid_annotations)

	tabix_obj.close()

	#Write annotations to best hits and final hits
	logger.debug("Annotated all peaks in chunk {0}. Now adding contents to queue...".format(idx))
	content = "\n".join([annopeak_to_string(peak, attributes=attributes) for peak in all_valid_annotations]) + "\n"
	q.put(("allhits.bed", idx, content))
	q.put(("allhits.txt", idx, content))
	content = ""
	
	finalhits_content = "\n".join([annopeak_to_string(peak, attributes=attributes) for peak in all_valid_annotations if peak.get("best_hit", 0) == 1]) + "\n"
	q.put(("finalhits.bed", idx, finalhits_content))
	q.put(("finalhits.txt", idx, finalhits_content))
	finalhits_content = ""
	
	## Hits per query if chosen
	if cfg_dict["output_by_query"] == True:
		query_names = [query["name"] for query in cfg_dict["queries"]]
		for name in query_names:
			query_str = "\n".join([annopeak_to_string(peak, attributes=attributes) for peak in all_valid_annotations if peak.get("query_name", "") == name]) + "\n"
			q.put((name + ".bed", idx, query_str))
			q.put((name + ".txt", idx, query_str))

	logger.debug("Job finished for chunk {0}".format(idx))
	return(0) #success

