#!/usr/bin/env pythons
from __future__ import division  #to allow float divisions (ovl_pk,ovl_feat) with 2 decimals
import os
import re 
import sys
import numpy as np 
import subprocess
from subprocess import PIPE
import shlex
import logging


def peak_has_chr (chrom , gtf_has_chr) :
	p_wo_chr  = "chr" not in chrom
	gtf_no_chr= not gtf_has_chr

	if (p_wo_chr and gtf_has_chr ): #Peak 'chr' should have chr if gtf has
		chrom_db = "chr"+chrom 

	elif  not p_wo_chr and not gtf_has_chr: #peak has chr, gtf doesn't-> remove  chr from peak
		chrom_db = chrom.strip("chr")

	elif  (gtf_no_chr and p_wo_chr ) or (gtf_has_chr and not p_wo_chr ): # none has chr -> keep p chrom
		chrom_db = chrom

	return (chrom_db)


def check4_chr (file):
	if os.path.exists(file) :
		with open(file, "r") as f:
			flines = f.readlines()
	
		comm_lines = len([li for li in flines if li.startswith("#")])
		first_line = flines [comm_lines]
		file_has_chr = first_line.startswith("chr")  # >> True / False 
		return (file_has_chr)


def tabix_index(annot_gtf) : 	
	
	""" Prepares gtf for query: Performs sorting, zipping and indexing of given gtf"""
	out_sorted= annot_gtf + ".sorted"
	out_zipped= out_sorted + ".gz"
		
	with open(out_zipped,'w') as sort_zipped :
		os.system('grep  -v  ^#  '+ annot_gtf+ '  |  sort -V  -k1,1 -k4,4 > '+ annot_gtf + '.sorted' )
		os.system('bgzip -c  -f ' + annot_gtf+'.sorted '+ ' > '+out_zipped  )	

	from subprocess import PIPE
	run_tabix = 'tabix -f  ' + out_zipped 
	idx = subprocess.Popen(shlex.split(run_tabix), stdout = subprocess.PIPE )  
	idx.wait()


def valid_fsb(h, q, pstrand) :
	"""Returns if a hit h is valid for query q in their basic common keys."""
	
	valid_query_keys = list(set(q.keys()) & set(h.keys()))
	if not  pstrand == None :
		q["strand"] = pstrand  #Peak's strand is the one  to be searched by Query.
		
	if(not all(map(lambda k: k in h, valid_query_keys))):
		return(False)
	else:
		return(all(map(lambda k: h[k] in q[k], valid_query_keys)))
	

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# def peaks_median(regions_file) : 
# 	with open(regions_file, 'r') as peaks:
# 		Lp=list()
# 		for p in peaks:
# 			try: 
# 				start,end = p.split("\t")[1], p.split("\t")[2]
# 				len_p = int(end) - int(start)
# 				Lp.append(len_p)
# 			except : 
# 				raise IOError("\nPeak file doesn't have correct format.Median couldn't be calculated !")
	
# 	#Lp_sorted = sorted(Lp)
# 	peak_Median = np.median(Lp)
# 	p_HalfMedian = peak_Median/2
# 	#logging.debug("\nMedian of peaks calculated for distance check:{} and 1/2 Median : {}".format(peak_Median,p_HalfMedian) )
# 	return (p_HalfMedian)

def distance_to_peak_center(p_center, hit3, hit4, strand, feat_pos):
	import operator
	
	feat_start = hit3 if strand == "+" else hit4
	feat_end   = hit4 if strand == "+" else hit3
	#logging.debug("\nClosest feature to be calculated now for the peak...")
	
	hit_center = np.mean([feat_start,feat_end])
	hit_pos = {"start": feat_start, "center":hit_center, "end":feat_end}
	d_pos = map(lambda i: abs(hit_pos[i] - p_center ), feat_pos)
	pos, dmin = min(enumerate(d_pos), key=operator.itemgetter(1))
	logging.debug("\n--> Positions and corresponding distances from Pk.center:")
	logging.debug(pos)
	logging.debug(dmin)
	
	min_pos = feat_pos[pos]
	#logging.debug("\n-->  Min distance = {} calculated from the feat.position : {}".format(dmin,min_pos))
	return min_pos,dmin

def find_hit_dir(fstart, fend, strand, pstart, p_center,pend) :

	feat_start = fstart if strand == "+" else fend
	feat_end   = fend if strand == "+" else fstart
	
	left_side_up  = (p_center - feat_start > 0) and (p_center - feat_end  > 0)
	right_side_up = (feat_start - p_center > 0) and (feat_end - p_center > 0)
	upstream = ((abs(pstart - feat_end)  >  abs(pstart - feat_start ))  and (abs (pend - feat_end) > abs(pend - feat_start) ))
	
	left_side_down  = (p_center - feat_end > 0) and (p_center - feat_start > 0)
	right_side_down = (feat_end - p_center > 0) and (feat_start - p_center > 0)
	downstream = ((abs(pstart - feat_end)  <  abs(pstart - feat_start ))  and (abs (pend - feat_end) < abs(pend- feat_start) ))
	
	if  upstream  and ( left_side_up or right_side_up ):
		return ("upstream")
	if downstream and (left_side_down or right_side_down):
		return("downstream")
	else:
		return("not.specified")


def define_direction(dir_key,fstart, fend,strand, p_len, pstart, pend, p_center) :  #if peak is stranded and negative, should be inversed
	
	hit_dir = find_hit_dir(fstart, fend, strand, pstart, p_center, pend)
	
	feat_start = fstart if strand == "+" else fend
	feat_end   = fend if strand == "+" else fstart
	ten_percent = p_len*0.1

	if abs(p_center - feat_start) >=  ten_percent :
		if hit_dir  == "upstream" and dir_key == ["upstream"]:
			##>  PC <--> TSS not closer than half of the peak
			#Dist(p_center - fstart) is larger than HalfMedian
			logging.debug("\n~~> Peak is Upstream to Hit {}-{},<{}>,as required by config!\n".format(feat_start,feat_end,strand))
			return (True)
		if hit_dir  == "downstream" and dir_key == ["downstream"]: 
			logging.debug( "\n~~> Peak is Downstream to Hit {}-{},<{}>,as required by config!\n".format(feat_start,feat_end,strand))
			return (True)
		else:
			return(False)
	
	if  abs(p_center - feat_start) < ten_percent  : 
		return(False)
		#logging.debug( "\n~~> Hit {}-{} cannot be chosen as Upstream because Distance(p_center - fstart) is shorter than 10 percent of peak.length\n".format(feat_start,feat_end))


def detect_internals(pstart, p_center, pend ,hit_start, hit_end, feat_pos):
	##Check for Internal_features (by default for genom_loc column, indep. of users key option)
	feat_in_peak = (pstart < hit_start and  hit_end < pend)
	peak_in_feat = (hit_start < pstart and  pend < hit_end)

	if feat_in_peak : 
		#logging.debug("\nThe feature is found internally to the peak region.")
		return ("True","FeatureInsidePeak" )
	elif peak_in_feat: 
		#logging.debug("\nThe peak is found internally to the feature.")
		return("False", "PeakInsideFeature")
	else : 
		return("False", "not.specified")


def overlap_peak_feature(genom_loc, peakL, featL, pstart, p_center, pend, hit_start, hit_end, hit_strand, feat_pos ):

	##A/ Find internal features/peaks
	is_internal, genom_loc = detect_internals(pstart, p_center, pend, hit_start, hit_end, feat_pos) #hit_start, hit_end : pos as given in gtf/no inversion for '-'strand.
	logging.debug("Is hit internal ? : {}".format(is_internal))
	
	##hit_start, hit_end are the real pos, considering strand, so if "-" strand: hit_end < hit_start, not correct for calculating range
	#st= hit_start if hit_start< hit_end else hit_end 
	#nd= hit_end if hit_end > hit_start else hit_start
	
	##B/ Find overlap of regions 
	p_range = range(pstart, pend)
	feat_range = range(hit_start, hit_end) # st < nd always for positive range
	pset = set(p_range)
	ovl_range = pset.intersection(feat_range)  

	#logging.debug("\nThe overlap length peak-feature is :{}".format(len(ovl_range)))

	all_pos = ["start", "end"]
	closest_pos, dmin = distance_to_peak_center(p_center, hit_start, hit_end,hit_strand, all_pos) 
	#logging.debug("\nClosest position to peak.center: {}".format(closest_pos))

	#C/ Define genomic_location of overlap
	if genom_loc == "not.specified" :
		if closest_pos == "end" and any(ovl_range) : 
			genom_loc = "overlapEnd"
		elif closest_pos == "start" and any(ovl_range):
			genom_loc = "overlapStart"
		elif not any(ovl_range) :
			#Check about direction :"upstream","downstream"
			genom_loc  = find_hit_dir(hit_start, hit_end, hit_strand, pstart,p_center,pend)
		
	logging.debug("\nGenomic Location :{}".format(genom_loc))
	
	# def round_up(ovl):
	# 	import math
	# 	ovl = math.ceil(ovl*100)/100
	# 	return(ovl)

	##D/ Calculate overlap percentage to peak and to feature
	#ovl_pk = Decimal(len(ovl_range))/ Decimal(peakL) #** Check values, if ratio >1 -> =1 
	peakL=1 if peakL==0 else peakL
	featL=1 if featL==0 else featL

	ovl_pk = len(ovl_range)/peakL
	ovl_pk = format(ovl_pk, '.2f')
	
	ovl_pk = 1 if float(ovl_pk)>1 else float(ovl_pk)
	#logging.debug ("\nOverlap over peak.length: {}/{}".format(len(ovl_range), peakL))
	#logging.debug ("\nRatio of ovl-to-peak.length : {}".format(ovl_pk))
	ovl_feat = len(ovl_range)/featL
	ovl_feat = format(ovl_feat, '.2f')
	#ovl_feat = round_up(float(ovl_feat)) if float(ovl_feat) == 0.00 else ovl_feat
	ovl_feat = 1 if float(ovl_feat) >1 else float(ovl_feat)
	#logging.debug("\nOverlap over feat.length: {}/{}".format(len(ovl_range),featL))
	#logging.debug("Ratio of ovl-to-feat.length : {}".format(ovl_feat))
	
	return genom_loc, ovl_pk, ovl_feat


def get_hit_attribute(hit, attribute):
	#for a in attrib_k :
	pos_match =  [i if re.match(attribute, hit_a) else None for i,hit_a in enumerate(hit[8].split("; ")) ]
	pos_match = filter(lambda x: x!=None, pos_match) 
	if len(pos_match) > 0 :
		attr_val = map(lambda m : hit[8].split("; ")[m].split(" ")[1].strip('"\'').rstrip('\";') , pos_match )
		val = [av for av in attr_val if av != None][0]
		val = val.replace("\t", "").replace("\r", "").replace("\n", "")
		#logging.debug("Attribute value found :{}".format(val))
		return (val)
	else :  # IF nowhere found match
		return ("not.found") 


def get_distance_by_dir ( query_distance, genom_loc, Dhit, remqD ):
	
	[D_upstr, D_downstr ] = query_distance #Always 2-distance values given-Also Dhit coming from besthit.function
	
	# return(d_best)
	if len(query_distance) >1 :
		if genom_loc == "upstream" or genom_loc == "overlapStart" :
			if Dhit <= remqD[0] and Dhit <= D_upstr :
				return (True)
			else:
				return (False)
		elif genom_loc == "downstream" or genom_loc == "overlapEnd" :
			if Dhit <= remqD[1] and Dhit <= D_downstr :
				return(True)
			else:
				return (False)
		else:
			if Dhit <= max(query_distance) :
				return (True)
			else:
				return (False)
	else : ## (if 1 dist.value):	
		return(query_distance[0])
		

def get_besthit (q,len_q_dist, p_nm, hit, attrib_keys, Dhit, min_dist): 

	Dhit = [Dhit,Dhit] if len_q_dist == 2 else Dhit

	if attrib_keys != ["None"] : 
		#attr_val = map(lambda k:  re.split(k+" ", hit[8])[1].split(';')[0].strip('"\'').rstrip('\"'), attrib_keys)
		attr_val =  map ( lambda a : get_hit_attribute(hit,a) ,attrib_keys)  #list of all values if multiple keys
		min_dist[q][p_nm] = [Dhit, [hit[2], hit[3], hit[4], hit[6], attr_val ] ]

	elif attrib_keys == ["None"]: 
		min_dist[q][p_nm] = [Dhit, [hit[2], hit[3], hit[4], hit[6] ] ]

	return min_dist[q][p_nm]


def create_table (peak_id, chrom, pstart, pend, p_center, min_dist_hit, attrib_keys, min_pos,genom_loc, ovl_pf, ovl_fp, i): 
	"""Saves info of the hit in a tabular form to be written in the output table. """
	import numpy as np
	#if qlen >1  :
	if attrib_keys != ["None"] :
		#extract min_dist_content
		[dist, [feat, fstart, fend, strand, attrib_val]] = min_dist_hit 
		#attrib_val.strip("\r").strip("\t").strip("\n")
 		#logging.debug("D(feat.pos - Peak center)= {}".format(dist) )
 		dist = max(dist) if type(dist) is list else dist
 		dist = '%d' % round(dist, 1)
		best_res =  "\t".join(np.hstack([peak_id, chrom, pstart, p_center, pend, feat, fstart, fend, strand, dist, min_pos, genom_loc, str(ovl_pf), str(ovl_fp), attrib_val, str(i) ]))
		return 	best_res+"\n"

	elif attrib_keys == ["None"]  : 
		[dist, [feat, fstart, fend, strand]]= min_dist_hit 
 		#logging.debug("D(feat.pos- Peak center)= {}".format(dist)  )
 		dist = max(dist) if type(dist) is list else dist
 		dist = '%d' % round(dist, 1)
		best_res = "\t".join([peak_id, chrom, pstart, p_center, pend,  feat, fstart, fend, strand, dist, min_pos, genom_loc, str(ovl_pf), str(ovl_fp), str(i) ])
		return 	best_res+"\n"

def write_hit_to_All(All_hits_tab, p_name, attrib_k, Dhit, hit, peak_id, chrom, pstart, pend, p_center, min_pos, genomic_location, ovl_pk, ovl_feat, i ):

	if attrib_k != ["None"] :
		#attr_val = map(lambda k: re.split(k+" ", hit[8])[1].split(';')[0].strip('"\'').rstrip('\"'), attrib_k)
		attr_val =  map ( lambda a : get_hit_attribute(hit,a), attrib_k )
		hit2add = [Dhit,  [hit[2], hit[3], hit[4], hit[6], attr_val ]]
		the_res = create_table(peak_id, chrom, pstart, pend, p_center, hit2add, attrib_k, min_pos, genomic_location, ovl_pk, ovl_feat, i )
	elif  attrib_k == ["None"] : 
		hit2add = [Dhit,  [hit[2], hit[3], hit[4], hit[6]]]
		the_res = create_table(peak_id, chrom, pstart, pend, p_center, hit2add, attrib_k, min_pos, genomic_location, ovl_pk, ovl_feat, i )
								
	if All_hits_tab[i][p_name] == '' or All_hits_tab[i][p_name].split("\t")[9] == "NA" :
		All_hits_tab[i][p_name] = the_res
		#logging.debug("\nHit to be saved to All_hits_tab, as first hit for this peak :\n{}".format(the_res))
									
	elif All_hits_tab[i][p_name] != '' or  All_hits_tab[i][p_name].split("\t")[9] != "NA":
		All_hits_tab[i][p_name] = All_hits_tab[i][p_name].strip("\n")
		All_hits_tab[i][p_name] = '\n'.join((All_hits_tab[i][p_name],the_res))		
		
	return (All_hits_tab[i][p_name])


def write_out_file(outfile,header_file, Table, header): 
	try :
		with open(outfile, "w") as of, open(header_file, "r") as hf : 
			of.write(hf.read())
			of.write(header+"\n")
			for k in Table:
				of.write("".join(Table[k]))
	except IOError :
		print ("\nUnable to open file " + outfile + " for writing results !" )


def merge_queries(Best_combo_k) :
	merged_q = map (lambda l : Best_combo_k[l].split("\t")[-1].strip("\n"), range(len(Best_combo_k)))
	#Read if combo_k is "" and give it the q.numb, so I have it ready for merging when one query =""
	merged_q[-1] = merged_q[-1]+"\n"
	merged_q = ",".join(merged_q)
	Best_combo_k_0 = "\t".join(Best_combo_k[0].split("\t")[:-1] )
	Best_merg_q = Best_combo_k_0 +"\t" +merged_q 
	return (Best_merg_q)
