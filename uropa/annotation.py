#!/usr/bin/env python3

"""Contains code for the annotation process"""
import pysam
from functools import reduce
import re
import numpy as np
import logging


def create_anno_dict(peak, hit=None):
	""" Returns a dictionary containing information on the hit from gtf """

	#Initialize dict with NAs
	keys = ["feature", "feat_strand", "feat_start", "feat_end", "feat_center", "feat_length", "feat_attributes", "distance", 
	        "feat_anchor", "query", "query_name", "best_hit", "relative_location", "feat_ovl_peak", "peak_ovl_feat"]
	anno_dict = {key:"NA" for key in keys}

	#Add peak information
	anno_dict.update(peak) #fills out peak chr/start/end/id/score/strand
	anno_dict["peak_center"] = int((anno_dict["peak_end"] + anno_dict["peak_start"])/2)
	anno_dict["peak_length"] = anno_dict["peak_end"] - anno_dict["peak_start"]

	#If hit was given, parse this as well
	if hit is not None:

		#Parse info from gtf string
		pairs = re.split(";\s*", hit.attributes) #regex remove 0 to n spaces
		pairs.remove("")
		attribute_dict = {pair.split()[0]:pair.split()[1].replace("\"", "") for pair in pairs} # parse " of attribute values

		# Fill in with feature info
		anno_dict["feature"] = hit.feature
		anno_dict["feat_strand"] = hit.strand
		anno_dict["feat_start"] = hit.start
		anno_dict["feat_end"] = hit.end
		anno_dict["feat_center"] = int((anno_dict["feat_end"] + anno_dict["feat_start"])/2)
		anno_dict["feat_length"] =  anno_dict["feat_end"] - anno_dict["feat_start"]
		anno_dict["feat_attributes"]  = attribute_dict

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

    #Calculate distances to each possible anchor
    raw_distances = [anno_dict["peak_center"] - anno_dict["anchor_pos"][anchor] for anchor in query_anchor]
    abs_distances = [abs(dist) for dist in raw_distances]
    min_dist_i = abs_distances.index(min(abs_distances))

    #Set minimum distance as best anchor
    anno_dict["raw_distance"] = raw_distances[min_dist_i]
    anno_dict["distance"] = abs(raw_distances[min_dist_i])
    anno_dict["feat_anchor"] = query_anchor[min_dist_i]

    return(anno_dict)


# import "division" allows decimals
def calculate_overlap(anno_dict):
    """ Calculates percentage of length covered by the peak/feature """
    
    peak_range = list(range(anno_dict["peak_start"], anno_dict["peak_end"]))
    feature_range = list(range(anno_dict["feat_start"], anno_dict["feat_end"]))
    ovl_range = set(peak_range).intersection(feature_range)
    
    ovl_pk = round(len(ovl_range) /  anno_dict["peak_length"], 3) 
    ovl_feat = round(len(ovl_range) / anno_dict["feat_length"], 3) 

    anno_dict["feat_ovl_peak"] = ovl_feat
    anno_dict["peak_ovl_feat"] = ovl_pk

    return(anno_dict)


def get_relative_location(anno_dict):
	""" Sets the relative location of peak to feature """

	if anno_dict["peak_start"] <= anno_dict["feat_start"] and anno_dict["peak_end"] >= anno_dict["feat_end"]:
		location = "FeatureInsidePeak"

	elif anno_dict["peak_start"] > anno_dict["feat_start"] and anno_dict["peak_end"] < anno_dict["feat_end"]:
		location = "PeakInsideFeature"

	elif anno_dict["feat_anchor"] == "start":
		if anno_dict["feat_ovl_peak"] > 0:
			location = "OverlapStart"
		else:
			location = "Upstream"

	elif anno_dict["feat_anchor"] == "end":
		if anno_dict["feat_ovl_peak"] > 0:
			location = "OverlapEnd"
		else:
			location = "Downstream"
	else:
		location = "NA"

	anno_dict["relative_location"] = location

	return(anno_dict)


def annotate_peaks(peaks, gtf_gz, gtf_index, cfg_dict, logger=None):
	""" Peaks is a list of tuple-elements (chrom, start, end, name, ...) 
		gtf_gz and gtf_index relate to the tabix gtf file
		cfg-dict is the loaded config containing queries
	"""

	if logger is None:
		logger = logging.getLogger('')	#local logger leading to nowhere

	#Open tabix file
	tabix_obj = pysam.TabixFile(gtf_gz, index=gtf_index)

	#Information on queries
	queries = cfg_dict["queries"]
	n_queries = len(queries)
	distances = sum([query["distance"] for query in queries], [])
	max_distance = int(max(distances))

	#For each peak in input peaks, collect all_valid_annotations
	all_valid_annotations = []
	for peak in peaks:
		logger.debug("Annotating peak: {0}".format(peak))

		#Fetch all possible hits from tabix
		extend_start = int(max(1, peak["peak_start"] - max_distance))
		extend_end = peak["peak_end"] + max_distance
		tabix_query = "{0}:{1}-{2}".format(peak["gtf_chr"], extend_start, extend_end)
		logger.debug("Tabix query: {0}".format(tabix_query))
		try:
			hits = tabix_obj.fetch(peak["peak_chr"], extend_start, extend_end, parser=pysam.asGTF())
		except ValueError:
			print("Could not fetch any hits for tabix {0}:{1}-{2}. Continueing.".format(peak["gtf_chr"], extend_start, extend_end))
			continue
		
		#Go through each hit from tabix and establish whether they are valid for queries
		valid_annotations = []
		stop_searching = False
		while stop_searching == False: # Loop will stop when stop_searching is true
			for hit in hits:
				logger.debug("Validating hit: {0}".format(hit))
				anno_dict = create_anno_dict(peak, hit)

				#Validate annotation for each peakquery
				stop_searching = False
				query_i = -1	#first query will be index 0
				while query_i+1 < n_queries and stop_searching == False:

					#Query information
					query_i += 1
					query = queries[query_i]	#current query to check
					anno_dict["query"] = query_i
					anno_dict["query_name"] = query["name"]
					
					#Calculate distances/relative location
					anno_dict = distance_to_peak_center(anno_dict, query["feature_anchor"])
					anno_dict = calculate_overlap(anno_dict)
					anno_dict = get_relative_location(anno_dict)

					##### Test validity of the hit to query_i ####
					checks = {}
					checks["feature"] = anno_dict["feature"] in query["feature"]	 #feature

					#Check feature anchor
					checks["feature_anchor"] = anno_dict["feat_anchor"] in query["feature_anchor"]

					#Peak strand relative to feature strand
					if query["strand"] != "ignore" and anno_dict["peak_strand"] != ".":
						checks["strand"].append((anno_dict["peak_strand"] == anno_dict["feat_strand"] and query["strand"] == "same") or 
												(anno_dict["peak_strand"] != anno_dict["feat_strand"] and query["strand"] == "opposite"))	

					#Check whether distance was valid
					if anno_dict["feat_strand"] == "+":
						checks["distance"] = anno_dict["raw_distance"] in range(-query["distance"][0], query["distance"][1])
					else:
						checks["distance"] = anno_dict["raw_distance"] in range(-query["distance"][1], query["distance"][0])

					#Check distance (Distance can still be valid if PeakInsideFeature/FeatureInsidePeak and internals flag is set)
					max_overlap = max(anno_dict["feat_ovl_peak"], anno_dict["peak_ovl_feat"])
					checks["distance"] = checks["distance"] or (query["internals"]*1.0 > 0 and max_overlap >= query["internals"]*1.0)	#if internals is set to more than 0 overlap

					#Filter on relative location 
					checks["relative_location"] = anno_dict["relative_location"] in query["relative_location"]
					
					#Filter on attribute if any was set
					if query["filter_attribute"] != None:
						checks["attribute"] = anno_dict["feat_attributes"].get(query["filter_attribute"], None) in query["attribute_values"]

					##### All checks are done -> establish if hit is a valid annotation #####
					logger.debug("Query {0} | Checks: {1} | Annotation: {2}".format(query_i+1, checks, {key:anno_dict[key] for key in anno_dict if key != "feat_attributes"}))

					valid = sum(checks.values()) == len(checks.values()) #all checks must be valid
					if valid:
						valid_annotations.append(anno_dict.copy())

					#Stop searching for queries fitting to hits if a hit was found and priority is true
					stop_searching = (valid and cfg_dict["priority"])
			
			#All tabix hits hits were checked
			stop_searching = True
	
		#After all hits have been checked; make final checks and set best flag
		if len(valid_annotations) > 0:	

			#If priority == True, find the highest ranked annotations for this peak
			if cfg_dict["priority"] == True:
				highest_priority_query = min([anno_dict["query"] for anno_dict in valid_annotations])
				logger.debug("Highest priority hit for {0} was {1}".format(peak, highest_priority_query))
				valid_annotations = [anno_dict for anno_dict in valid_annotations if anno_dict["query"] == highest_priority_query]

			distances = [anno_dict["distance"] for anno_dict in valid_annotations]
			valid_annotations[distances.index(min(distances))]["best_hit"] = 1

		else:
			valid_annotations = [create_anno_dict(peak)]	#empty hit
			valid_annotations[0]["best_hit"] = 1			#the empty hit is the best hit

		#Add result to all the valid annotations 
		all_valid_annotations.extend(valid_annotations)

	tabix_obj.close()

	return(all_valid_annotations)
