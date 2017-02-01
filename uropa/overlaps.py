#!/usr/bin/env python
"""Contains functions for UROPA overlap evaluation."""
from __future__ import division
import os
import re
import sys
import subprocess
import logging
import shlex
import shutil
import glob
import numpy as np


def peak_has_chr(chrom, gtf_has_chr):
    """Checks if the peak chromosome name against the reference chromosome name."""
    p_wo_chr = "chr" not in chrom
    gtf_no_chr = not gtf_has_chr

    if p_wo_chr and gtf_has_chr:  # Peak 'chr' should have chr if gtf has
        chrom_db = "chr" + chrom

    elif not p_wo_chr and not gtf_has_chr:  # peak has chr, gtf doesn't-> remove  chr from peak
        chrom_db = chrom.strip("chr")

    elif (gtf_no_chr and p_wo_chr) or (gtf_has_chr and not p_wo_chr):  # none has chr -> keep p chrom
        chrom_db = chrom

    return chrom_db


def check4_chr(file):
    """Checks if a file has lines starting with 'chr'."""
    if os.path.exists(file):
        with open(file, "r") as f:
            flines = f.readlines()

        comm_lines = len([li for li in flines if li.startswith("#")])
        first_line = flines[comm_lines]
        file_has_chr = first_line.startswith("chr")  # >> True / False
        return file_has_chr


def tabix_index(annot_gtf):
    """ Prepares gtf for query: Performs sorting, zipping and indexing of given gtf"""
    out_sorted = annot_gtf + ".sorted"
    out_zipped = out_sorted + ".gz"

    with open(out_zipped, 'w'):
        os.system('grep  -v  ^#  ' + annot_gtf +
                  '  |  sort -V  -k1,1 -k4,4 > ' + annot_gtf + '.sorted')
        os.system('bgzip -c  -f ' + annot_gtf +
                  '.sorted ' + ' > ' + out_zipped)

    run_tabix = 'tabix -f  ' + out_zipped
    idx = subprocess.Popen(shlex.split(run_tabix), stdout=subprocess.PIPE)
    idx.wait()


def valid_fsa(h, hit, q, pstrand):
    """Returns if a hit h is valid for query q in their basic common keys."""

    vf = (h["feature"] == q["feature"][0])
    v_str = valid_strand(h["strand"], pstrand, q["strand"][0])
    va = valid_attribute(q["filter.attribute"][0], q["attribute.value"][0], hit)
    return all([vf, v_str, va])


def valid_strand(hit_str, p_str, q_str):
    """Returns boolean showing match of peak.strand to feature.strand according to query requirements """
    if p_str != ".":
        if q_str == "ignore":
            return True if (hit_str != p_str) or (hit_str == p_str) else False
        if q_str == "same":
            return True if (hit_str == p_str) else False
        if q_str == "opposite":
            return True if (hit_str == "+" and p_str == "-") or (hit_str == "-" and p_str == "+") else False
            # OR : return (True if (hit_str != p_str) ,i.e when one is "." and
            # other is "+,-"

    elif p_str == "." or hit_str == ".":
        return True


def valid_attribute(attr_filter_key, attr_filter_val, hit):
    """Validates the hit according to a filter attribute."""
    if (attr_filter_key != "None") and (attr_filter_val != "None"):
        try:
            # If key for filtering is not correct or doesn't exist-> error
            # should be ignored
            hit_attrib_val = re.split(
                "; " + attr_filter_key + " ", hit[8])[1].split(';')[0].strip('"\'').rstrip('\"')
        except IndexError:  # if key doesn't exist re.split will give error
            hit_attrib_val = "not.found"

        # If biotype of hit == attr_value from query-> continue annotation
        return attr_filter_val == hit_attrib_val
    else:
        return True  # no filtering given->ignore


def file_len(fname):
    """Returns Number of lines of a file"""
    with open(fname) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


def parse_peak(peakstr, extend=0, delim='\t'):
    """ Parses a string into peak dictionaries """
    fields = peakstr.replace('\n', '').replace('\r', '').split(delim)
    num_fields = len(fields)

    if num_fields < 3:
        return None

    p = dict()
    if num_fields >= 3:
        p['chr'] = fields[0]
        p['start'] = fields[1]
        p['end'] = fields[2]

    if num_fields >= 4:
        if fields[3] != '.':
            p['name'] = fields[3]

    if num_fields >= 5:
        p['score'] = fields[4]

    if num_fields >= 6:
        p['strand'] = fields[5]

    defaults = {'id': p['chr'] + ":" + p['start'] + "-" + p['end'], 'name': p['chr'] + ":" + p['start'] + "-" + p['end'], 'score': 0, 'strand': ".",
                'center': int(np.around(np.mean([int(p['start']), int(p['end'])]))), 'estart': max(1, int(p['start']) - extend), 'eend': int(p['end']) + extend, 'length': abs(int(p['end']) - int(p['start']))}
    if 'name' in p.keys():
        p['id'] = p['chr'] + ":" + p['start'] + "-" + p['end'] + "_" + p['name']

    values = [p[k] if k in p else defaults[k] for k in defaults.keys()]
    peak = dict(zip(p.keys() + defaults.keys(), p.values() + values))
    return peak


def define_direction(dir_key, fstart, fend, strand, p_len, pstart, pend, p_center):
    """Verifies if direction of peak is the same as required by query"""

    peak_dir = find_peak_dir(fstart, fend, strand, pstart, p_center, pend)
# Inverse in case of negative strand
    feat_start = fstart if strand == "+" else fend

# How much internally to peak can a feature be, to be labeled as upstr/downstr.
    ten_percent = p_len * 0.1

    if abs(p_center - feat_start) >= ten_percent:
        if peak_dir == "upstream" and dir_key == ["upstream"]:
            return True
        return peak_dir == "downstream" and dir_key == ["downstream"]

    if abs(p_center - feat_start) < ten_percent:
        return False


def distance_to_peak_center(p_center, hit3, hit4, strand, feat_pos):
    """Returns the position of feature from which the distance is minimum to the peak and the measured distance to peak center"""
    import operator

    feat_start = hit3 if strand == "+" else hit4
    feat_end = hit4 if strand == "+" else hit3

    hit_center = np.mean([feat_start, feat_end])
    hit_pos = {"start": feat_start, "center": hit_center, "end": feat_end}
    d_pos = map(lambda i: abs(hit_pos[i] - p_center), feat_pos)
    pos, dmin = min(enumerate(d_pos), key=operator.itemgetter(1))

    min_pos = feat_pos[pos]
    return min_pos, dmin


def find_peak_dir(fstart, fend, strand, pstart, p_center, pend):
    """ Returns the location of the  queried peak relative to the feature direction """
    feat_start = fstart if strand == "+" else fend
    feat_end = fend if strand == "+" else fstart

    # Add one base to single-base features to give length for direction
    # detection.
    if feat_start == feat_end and strand == "+":
        feat_end = feat_start + 1
    elif feat_start == feat_end and strand == "-":
        feat_start = feat_end + 1

    up_sides = abs(p_center - feat_start) < abs(p_center -
                                                feat_end)  # left and right
    down_sides = abs(p_center - feat_start) > abs(p_center - feat_end)

    upstream = ((abs(pstart - feat_end) > abs(pstart - feat_start))
                and (abs(pend - feat_end) > abs(pend - feat_start)))
    downstream = ((abs(pstart - feat_end) < abs(pstart - feat_start))
                  and (abs(pend - feat_end) < abs(pend - feat_start)))

    if upstream and up_sides:
        return "upstream"
    elif downstream and down_sides:
        return "downstream"
    else:
        return "not.specified"


def find_internals_dir(anchor, p_center, feat_start, feat_end, strand):
    """ Determine the direction of peak when feature-inside-peak or peak-inside-feature """
    # +strand: When internal feature/peak is Left of p.center, dir->downstream, otherwise dir-> upstream,
    # -strand :inverse of above
    feat_center = np.mean([feat_start, feat_end])
    feat_pos = {"start": feat_start, "center": feat_center, "end": feat_end}
    if strand == "+":
        return "downstream" if feat_pos[anchor] < p_center else "upstream"

    if strand == "-":
        return "upstream" if feat_pos[anchor] < p_center else "downstream"


def get_distance_by_dir(inputD, genom_loc, intern_loc, Dhit):
    """Limits the hit by a distance window depending on peak's position relative-to-feature """

    [D_upstr, D_downstr] = inputD

    if genom_loc == "upstream" or genom_loc == "overlapStart":
        return Dhit <= D_upstr
    if genom_loc == "downstream" or genom_loc == "overlapEnd":
        return Dhit <= D_downstr

    # Rescue if internal peak
    return(any(intern_loc))


def detect_internals(pstart, pend, hit_start, hit_end):
    """[Local] Check for internal features (for 'genomic_location' column, independent of users key option) """

    feat_in_peak = (pstart < hit_start and hit_end < pend)
    peak_in_feat = (hit_start < pstart and pend < hit_end)

    if feat_in_peak:
        return "FeatureInsidePeak"
    elif peak_in_feat:
        return "PeakInsideFeature"
    else:
        return "not.specified"


def round_up(val):
    """[Local] Rounds a value on second decimal """
    import math
    val = math.ceil(val * 100) / 100
    return val


# import "division" allows decimals
def calculate_overlap(pstart, pend, peakL, featL, hit_start, hit_end):
    """[Local] Returns value of overlap btw {0,1} representing percentage of length covered by the peak and that covered by the feature """
    p_range = range(pstart, pend)
    feat_range = range(hit_start, hit_end)
    pset = set(p_range)

    ovl_range = pset.intersection(feat_range)
    peakL = 1 if peakL == 0 else peakL
    featL = 1 if featL == 0 else featL

    ovl_pk = round_up(len(ovl_range) / peakL)
    ovl_pk = 1 if ovl_pk > 1 else ovl_pk
    ovl_feat = round_up(len(ovl_range) / featL)
    ovl_feat = 1 if ovl_feat > 1 else ovl_feat

    return ovl_pk, ovl_feat, ovl_range


def define_genom_loc(current_loc, pstart, p_center, pend, hit_start, hit_end, hit_strand, ovl_range):
    """ [Local] Returns location label to be given to the annotated peak, if upstream/downstream or overlapping one edge of feature."""
    all_pos = ["start", "end"]
    closest_pos, dmin = distance_to_peak_center(
        p_center, hit_start, hit_end, hit_strand, all_pos)
    if current_loc == "not.specified":  # Not internal
        if closest_pos == "end" and any(ovl_range):
            return "overlapEnd"
        elif closest_pos == "start" and any(ovl_range):
            return "overlapStart"
        elif not any(ovl_range):
            # Check about direction :"upstream", "downstream"
            current_loc = find_peak_dir(
                hit_start, hit_end, hit_strand, pstart, p_center, pend)
            return current_loc
    return current_loc


def overlap_peak_feature(genom_loc, pstart, p_center, pend, peakL, featL, hit_start, hit_end, hit_strand):
    """Gives the collective information of the location and overlap of a peak to a feature """
    # A/ Find internal features/peaks
    # hit_start, hit_end : as given in gtf/no inversion for '-'strand.
    genom_loc = detect_internals(pstart, pend, hit_start, hit_end)
    # B/ Calculate overlap Ratio peak/feat and feat/peak
    ovl_pk, ovl_feat, ovl_range = calculate_overlap(
        pstart, pend, peakL, featL, hit_start, hit_end)

    # C/ Define genomic_location with or w/o overlap (input is internals
    # genom_loc for comparison and update )
    genom_loc = define_genom_loc(
        genom_loc, pstart, p_center, pend, hit_start, hit_end, hit_strand, ovl_range)
    return genom_loc, ovl_pk, ovl_feat


def get_hit_attribute(hit, attribute):
    """Splits attributes from hit lines"""
    pos_match = [i if re.match(
        attribute, hit_a) else None for i, hit_a in enumerate(hit[8].split("; "))]
    pos_match = filter(lambda x: x is not None, pos_match)
    if len(pos_match) > 0:
        attr_val = map(lambda m: hit[8].split("; ")[m].split(" ")[
            1].strip('"\'').rstrip('\";'), pos_match)
        val = [av for av in attr_val if av is not None][0]
        val = val.replace("\t", "").replace("\r", "").replace("\n", "")
        return val
    else:
        return "not.found"


def get_besthit(q, len_q_dist, p_nm, hit, attrib_keys, Dhit, min_dist):
    """Defines the best hit for a query."""
    Dhit = [Dhit, Dhit] if len_q_dist == 2 else Dhit

    if attrib_keys != ["None"]:
        #attr_val = map(lambda k:  re.split(k+" ", hit[8])[1].split(';')[0].strip('"\'').rstrip('\"'), attrib_keys)
        # list of all values if multiple keys
        attr_val = map(lambda a: get_hit_attribute(hit, a), attrib_keys)
        min_dist[q][p_nm] = [Dhit, [hit[2], hit[3], hit[4], hit[6], attr_val]]

    elif attrib_keys == ["None"]:
        min_dist[q][p_nm] = [Dhit, [hit[2], hit[3], hit[4], hit[6]]]

    return min_dist[q][p_nm]


def create_table(peak_id, chrom, pstart, pend, p_center, min_dist_hit, attrib_keys, min_pos, genom_loc, ovl_pf, ovl_fp, i):
    """Saves info of the hit in a tabular form to be written in the output table. """
    if attrib_keys != ["None"]:
        # extract min_dist_content
        [dist, [feat, fstart, fend, strand, attrib_val]] = min_dist_hit
        # attrib_val.strip("\r").strip("\t").strip("\n")
        dist = max(dist) if isinstance(dist, list) else dist
        dist = '%d' % round(dist, 1)
        best_res = "\t".join(np.hstack([peak_id, chrom, pstart, p_center, pend, feat, fstart,
                                        fend, strand, min_pos, dist, genom_loc, str(ovl_pf), str(ovl_fp), attrib_val, str(i)]))
        return best_res + "\n"

    elif attrib_keys == ["None"]:
        [dist, [feat, fstart, fend, strand]] = min_dist_hit
        dist = max(dist) if isinstance(dist, list) else dist
        dist = '%d' % round(dist, 1)
        best_res = "\t".join([peak_id, chrom, pstart, p_center, pend, feat, fstart,
                              fend, strand, min_pos, dist, genom_loc, str(ovl_pf), str(ovl_fp), str(i)])
        return best_res + "\n"


def write_hit_to_All(All_hits_tab, p_name, attrib_k, Dhit, hit, peak_id, chrom, pstart, pend, p_center, min_pos, genomic_location, ovl_pk, ovl_feat, j):
    """Writes an output table."""
    if attrib_k != ["None"]:
        attr_val = map(lambda a: get_hit_attribute(hit, a), attrib_k)
        hit2add = [Dhit, [hit[2], hit[3], hit[4], hit[6], attr_val]]
        the_res = create_table(peak_id, chrom, pstart, pend, p_center,
                               hit2add, attrib_k, min_pos, genomic_location, ovl_pk, ovl_feat, j)
    elif attrib_k == ["None"]:
        hit2add = [Dhit, [hit[2], hit[3], hit[4], hit[6]]]
        the_res = create_table(peak_id, chrom, pstart, pend, p_center,
                               hit2add, attrib_k, min_pos, genomic_location, ovl_pk, ovl_feat, j)

    if All_hits_tab[j][p_name] == '' or All_hits_tab[j][p_name].split("\t")[9] == "NA":
        All_hits_tab[j][p_name] = the_res

    elif All_hits_tab[j][p_name] != '' or All_hits_tab[j][p_name].split("\t")[9] != "NA":
        All_hits_tab[j][p_name] = All_hits_tab[j][p_name].strip("\n")
        All_hits_tab[j][p_name] = '\n'.join((All_hits_tab[j][p_name], the_res))

    return All_hits_tab[j][p_name]


def concat_comments(queries, priority, annot_gtf, peaks_bed):
    """Puts together comments for file header."""
    comments = ["#UROPA-Universal RObust Peak Annotator"]
    for q in enumerate(queries):
        comments.append("#Query No {} :".format(q[0]))
        comments.append("#feature: {}, strand: {}, feature.anchor: {}, distance : {} , direction : {}, internals :{},\n#show.attribute(s): {}, filter.attribute: {},attribute.value:{}".format(
                q[1]['feature'], q[1]['strand'], q[1]['feature.anchor'], q[
                    1]['distance'], q[1]['direction'], q[1]['internals'],
                q[1]['show.attributes'], q[1]['filter.attribute'], q[1]['attribute.value']))
    comments.append("#priority:{}".format(priority))
    comments.append("#GTF: {}".format(annot_gtf))
    comments.append("#BED: {}".format(peaks_bed))
    comments.append("#Columns.terminology:")
    comments.append("#feature, feature_start, feature_end, feature_strand: The information of the genomic feature that annotates the peak, as extracted by the gtf file.")
    comments.append(
            "#distance:The distance measured as following: abs(peak.center-feature.anchor).If no feature.anchor given,then the minimum of 3 distances from each feature.anchor{start,center,end} to peak.center is chosen.")
    comments.append("#feat_anchor : The position of the genomic feature chosen for annotation that had the minimum distance to the peak.center.If feature.anchor given in config this will be shown also here.")
    comments.append(
            "#genomic_location: The position of the peak relative to the annotated feature direction.")
    comments.append("#feat_ovl_peak : When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / peak.length) shows percentage of peak covered by the feature.(i.e 1.0 = 100% of peak covered, peak is internal.")
    comments.append("#peak_ovl_feat : When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / feature.length) shows percentage of feature covered by the peak.(i.e 1.0 = 100% of feature covered, feature is internal.)")
    comments.append("#Attributes that have been given in the key 'show.atttributes' will be shown here and their values extracted by the gtf will be displayed for each feature.If 'filter.attribute' contains same attribute, this column helps confirm the filtering.")
    comments.append("#query:The query that validates with its given parameters the feature to be assigned to the peak.If only one query given, column will always display '0',the first query.")
    comments.append("#---------------------------------------------------------------------------------------------------------------------------------------#")

    return '\n'.join(comments)

def write_partial_file(outfile, Table):
    """Writes a partial file."""
    with open(outfile, "w") as of:
        for k in Table:
            of.write("".join(Table[k]))


def merge_queries(Best_combo_k):
    """Merges queries."""
    merged_q = map(lambda l: Best_combo_k[l].split(
        "\t")[-1].strip("\n"), range(len(Best_combo_k)))
    # Read if combo_k is "" and give it the q.numb, so I have it ready for
    # merging when one query =""
    merged_q[-1] = merged_q[-1] + "\n"
    joined_q = ",".join(merged_q)
    Best_combo_k_0 = "\t".join(Best_combo_k[0].split("\t")[:-1])
    Best_merg_q = Best_combo_k_0 + "\t" + joined_q
    return Best_merg_q

def finalize_file(ffile, partials, header, comments=None, log=None):
    """Writes a output table of UROPA."""
    try:
        with open(ffile, "w") as f:
            if not comments is None:
                f.write(comments+'\n')
            f.write(header+'\n')
            for p in partials:
                with open(p) as pf:
                    shutil.copyfileobj(pf, f)
    except IOError:
        if not log is None:
            log.error("Unable to write to file {}".format(ffile))

def cleanup(directory, log=None):
    """Removes temporary files from a UROPA directory."""
    temp_files = glob.glob(directory + '*_part_*')
    for f in temp_files:
        try:
            os.remove(f)
        except OSError:
            if not log is None:
                log.error("Could not remove temporary file {}".format(f))
            continue
