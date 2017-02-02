"""Contains code for annotation process."""
import sys
import operator
import numpy as np
import pysam
import overlaps as ovls


def annotation_process(input_args, peak_file, log=None):
    """Contains main logic for the annotation process."""
    [outdir, gtf_index, attrib_k, queries, max_distance,
     priority, gtf_has_chr] = input_args

    try:
        anno = pysam.TabixFile(gtf_index)
    except IOError:
        log.error("Unable to open tabix index {}.".format(gtf_index))
    except ValueError:
        log.error("Tabix index file is missing ({})".format(gtf_index))

    try:
        prefix_pk = peak_file.split("_peak_")[1]
    except IndexError:
        # In case peaks file is small and not splitted
        prefix_pk = ""

    with open(peak_file, 'r') as peaks:
        Best_hits_tab = dict()
        All_hits_tab = dict()
        min_dist = dict()

        from collections import OrderedDict
        for j in range(len(queries)):
            min_dist[j] = dict()
            Best_hits_tab[j] = OrderedDict()
            All_hits_tab[j] = OrderedDict()

        counter = 0
        for p in peaks:
            counter += 1

            peak = ovls.parse_peak(p, extend=max_distance)
            if peak is None:
                if log is not None:
                    log.warning("Skipping invalid peak '{}'".format(p))
                continue
            #peak['id'] = peak['name'] if peak[
            #    'name'] is not None else peak['id']
            # Re-initialise table records for each peak
            for q in enumerate(queries):
                All_hits_tab[q[0]][peak['id']] = ""
                Best_hits_tab[q[0]][peak['id']] = ""

                q[1]["distance"] = [abs(int(d)) for d in q[1]["distance"]]
                if len(q[1]["distance"]) == 2:
                    min_dist[q[0]][peak['id']] = [q[1]["distance"], list()]
                else:
                    min_dist[q[0]][peak['id']] = [q[1]["distance"][0], list()]

            # Run TABIX
            chrom_db = ovls.peak_has_chr(peak['chr'], gtf_has_chr)
            tabix_query = chrom_db + ":" + \
                str(peak['estart']) + '-' + str(peak['eend'])

            try:
                hits = anno.fetch(tabix_query, multiple_iterators=True)
            except ValueError:
                hits = list()
                if log is not None:
                    log.warning("Region {} could not be found in GTF annotation for peak {}. Tabix query was: {}-{}".format(
                        chrom_db, peak['id'], str(peak['estart']), str(peak['eend'])))

            has_hits = list()
            # keep array of  all valid queries (T,F) for all hits in the peak.
            valid_q_per_peak = list()
            dict_vqp = dict()

            # Collection and analysis of all hits for the peak
            for hit in hits:  # All overlapping features
                hit = hit.split("\t")  # from "anno.fetch" hit is a string
                h = {'feature': hit[2], 'strand': hit[6]}
                hit_center = np.mean([int(hit[3]), int(hit[4])])

                dist_from_peak = min(
                    abs(int(peak['estart']) - int(hit[3])),
                    abs(int(peak['start']) - int(hit[3])),
                    abs(int(peak['eend']) - int(hit[3])),
                    abs(int(peak['end']) - int(hit[3])),
                    abs(int(peak['eend']) - int(hit[4])),
                    abs(int(peak['end']) - int(hit[4])),
                    abs(int(peak['estart']) - int(hit[4])),
                    abs(int(peak['start']) - int(hit[4])),
                    abs(peak['center'] - hit_center),
                    abs(peak['center'] - int(hit[3])),
                    abs(peak['center'] - int(hit[4])))
                # Verify that hit is valid at least for one of the distances of
                # queries
                valid_dist = any([dist_from_peak <= int(
                    max(q["distance"])) for q in queries])
                # Keep hit if internals are required in any query
                i_want_internals = any([q["internals"] in [
                    ['T'], ['True'], ['TRUE'], ['Yes'], ['YES'], ['Y'], ['yes'], ['F'], ['False'], ['FALSE'], ['No'], ['NO'], ['N'], ['no']] for q in queries])

                if (i_want_internals) and not valid_dist:
                    # Keep if gene inside the peak even if Dist > config.D
                    feat_in_peak = (int(peak['start']) < int(
                        hit[3]) and int(hit[4]) < int(peak['end']))
                    peak_in_feat = (int(hit[3]) < int(
                        peak['start']) and int(peak['end']) < int(hit[4]))

                    if feat_in_peak or peak_in_feat:
                        valid_dist = True

                # Find hits with valid values for the queries (Search all
                # queries ,Not only PRIORITY)
                v_fsa = map(lambda q: ovls.valid_fsa(h, hit, q, peak['strand']), queries)

                # Pair the Valid query values(fsb) with valid_distance and
                # valid strand for each query
                vsd = [[x, valid_dist] for x in v_fsa]
                valid_queries = [i for i, v in enumerate(vsd) if all(v)]

                hitj = "\t".join(hit)
                # Create dictionary of hit with its valid query per peak
                if valid_queries:
                    has_hits.append(True)
                    valid_q_per_peak.append(valid_queries)
                    dict_vqp.update({hitj: valid_queries})

                if not valid_queries:
                    has_hits.append(False)

            # ----- All hits parsed. Check only hits with valid-queries now ----- #
            #log.debug("\n---All hits parsed for the peak.Totally, the Peak has {} hits from which {} are Valid ---".format( len(has_hits), has_hits.count(True) ))
            # 9 cols= feat, f.start, f.end, f.strand, dist, min_pos, genom_loc,
            # feat-to-peak-ovl , peak-to-feat-ovl (no Q)
            nas_len = len(attrib_k) + 9
            NAsList_q = list(np.repeat("NA", nas_len))

            # Search hits with only Prior or Secondary Queries
            for hitj, vq in dict_vqp.items():
                hit = hitj.split("\t")
                hit_len = abs(int(hit[4]) - int(hit[3]))
                strand = hit[6]
                for j in vq:
                    # Check DIRECTION before Closest_Distance, if given
                    if queries[j]["direction"] != ['any_direction']:
                        correct_dir = ovls.define_direction(queries[j]["direction"], int(hit[3]), int(
                            hit[4]), strand, peak['length'], int(peak['start']), int(peak['end']), peak['center'])
                        #logger.debug("\nFor the hit {}-{}, direction is correct : {}".format(hit[3],hit[4] ,correct_dir))

                        if correct_dir:
                            # IF direction of hit is the desired, then filter
                            # for Distance
                            min_pos, Dhit = ovls.distance_to_peak_center(peak['center'], int(
                                hit[3]), int(hit[4]), strand, queries[j]["feature.anchor"])
                            #logger.debug("\nClosest Distance from the peak center : {} ".format(Dhit))

                        if not correct_dir and Best_hits_tab[j][peak['id']] == "" and All_hits_tab[j][peak['id']] == "":
                            # hit with Incorrect Dir: move to new peak, fill in NAs if  peak is empty
                            #log.debug("\nThe hit doesn't have the correct direction -> NAs in All & Best hits table -> Continue to New hit.")
                            All_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                                'start'], peak['center'], peak['end'], NAsList_q, str(j) + "\n"]))
                            Best_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                                'start'], peak['center'], peak['end'], NAsList_q, str(j) + "\n"]))
                            continue  # Move to next valid query and then next hit

                        # When direction NOT correct but tables not empty.
                        elif not correct_dir and Best_hits_tab[j][peak['id']] != "" and All_hits_tab[j][peak['id']] != "":
                            continue

                    elif queries[j]['direction'] == ['any_direction']:
                        min_pos, Dhit = ovls.distance_to_peak_center(peak['center'], int(
                            hit[3]), int(hit[4]), strand, queries[j]["feature.anchor"])
                        #log.debug("\nClosest Distance(Dhit) when No Direction defined :{} ".format(Dhit))

                    # > Check OVERLAPS of peak-hit, define genomic_location
                    genomic_location = "not.specified"
                    genomic_location, ovl_pk, ovl_feat = ovls.overlap_peak_feature(genomic_location, int(
                        peak['start']), peak['center'], int(peak['end']), peak['length'], hit_len, int(hit[3]), int(hit[4]), strand)

                    # > After Direction is checked move on to check Distance hit <--> peak
                    same_gene = all(x in min_dist[j][peak['id']][1] for x in [hit[2], hit[3], hit[
                        4], hit[6]])  # next hit shouldn't have same {feat,start,end}
                    internals_location = list()
                    if "Inside" in genomic_location:
                        # > Check internals direction for defining Bi-direct. distance window
                        internals_location = [ovls.find_internals_dir(a, peak['center'], int(hit[3]), int(hit[4]), strand) for a in queries[j]["feature.anchor"]]

                    if len(queries[j]["distance"]) == 2:
                        d_is_best = ovls.get_distance_by_dir([min_dist[j][peak['id']][0][0], min_dist[
                            j][peak['id']][0][1]], genomic_location, internals_location, Dhit)
                    if len(queries[j]["distance"]) == 1:
                        d_is_best = ovls.get_distance_by_dir([min_dist[j][peak['id']][0], min_dist[j][
                            peak['id']][0]], genomic_location, internals_location, Dhit)

                    # print "Best distance found :{}".format(d_is_best)
                    if d_is_best and not same_gene:  # Dhit < Dbest
                        #log.debug("\nDistance of Hit from Peak Center = {}, INFERIOR to current Min Distance = {} ".format(Dhit, min_dist[j][peak['id']][0]))
                        min_dist[j][peak['id']] = ovls.get_besthit(j, len(queries[j]["distance"]), peak[
                            'id'], hit, attrib_k, Dhit, min_dist)
                        #print("Minimum distance updated: {}".format(min_dist[j][peak['id']][0]))
                        Best_res = ovls.create_table(peak['name'], peak['chr'], peak['start'], peak['end'], str(
                            peak['center']), min_dist[j][peak['id']], attrib_k, min_pos, genomic_location, ovl_pk, ovl_feat, j)
                        Best_hits_tab[j][peak['id']] = Best_res

                    # Dhit > Dbest
                    # only if empty fill in with NAs
                    elif not d_is_best and not same_gene and Best_hits_tab[j][peak['id']] == "":
                        #log.debug("\nDistance of Hit from Peak Center = {}, LARGER THAN current Min Distance = {}\n".format(Dhit, min_dist[j][peak['id']][0]))
                        Best_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                            'start'], str(peak['center']), peak['end'], NAsList_q, str(j) + "\n"]))

                    # EVERY HIT getting registered in Allhits file if Dhit <
                    # query.distance
                    if len(queries[j]["distance"]) > 1:
                        Dhit_smaller = ovls.get_distance_by_dir([queries[j]["distance"][0], queries[j][
                            "distance"][1]], genomic_location, internals_location, Dhit)
                    else:
                        Dhit_smaller = ovls.get_distance_by_dir([queries[j]["distance"][0], queries[j][
                            "distance"][0]], genomic_location, internals_location, Dhit)

                    if Dhit_smaller and not same_gene:
                        #log.debug("Distance of hit SMALLER than Config Distance -> Hit written to All_Hits.")
                        All_hits_tab[j][peak['id']] = ovls.write_hit_to_All(All_hits_tab, peak['id'], attrib_k, Dhit, hit, peak['name'], peak['chr'], peak['start'],
                                                                            peak['end'], str(peak['center']), min_pos, genomic_location, ovl_pk, ovl_feat, j)

                    # Hit not fitting in any of the distance values
                    if not Dhit_smaller and queries[j]["internals"] != ["True"] and (All_hits_tab[j][peak['id']] == ''):
                        #log.debug("\nDhit= {} is LARGER than config Distance:{}.".format(Dhit, queries[j]["distance"]))
                        # Write over empty or NA the new NA, for new hit,so
                        # each hit is parsed.
                        All_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                            'start'], str(peak['center']), peak['end'], NAsList_q, str(j) + "\n"]))

                    # Hits with further Distance -> Check for Internals
                    if not Dhit_smaller and queries[j]["internals"] == ["True"] and not same_gene:
                        if "Inside" in genomic_location:
                            #log.debug("\n-> Hit is 'Internal' with distance LARGER than config.distance.It will be recorded to the All_hits table.")
                            All_hits_tab[j][peak['id']] = ovls.write_hit_to_All(All_hits_tab, peak['id'], attrib_k, Dhit, hit, peak['name'], peak['chr'], peak['start'], peak['end'], str(peak['center']),
                                                                                min_pos, genomic_location, ovl_pk, ovl_feat, j)

                    if not Dhit_smaller and All_hits_tab[j][peak['id']] != '':
                        #log.debug("Hit has larger distance than allowed ")
                        continue

            # > Add to Best Hits the Best Internal features(when internals=True, D>config."distance"),
            # after having filled-in the All Hits for the peak.
            for hitj, vq in dict_vqp.items():
                for j in vq:
                    if Best_hits_tab[j][peak['id']] != "" and All_hits_tab[j][peak['id']] != "":
                        if (Best_hits_tab[j][peak['id']].split("\t")[10] == "NA" and
                                All_hits_tab[j][peak['id']].split("\t")[10] != "NA" and
                                queries[j]["internals"] == ["True"]):

                            hit_line = All_hits_tab[j][peak['id']].split("\n")
                            hit_line = [h for h in hit_line if h != '']
                            internal = map(
                                lambda h: h.split("\t")[11], hit_line)
                            hit_dist = map(lambda h: int(
                                h.split("\t")[10]), hit_line)
                            mv_pos, min_val = min(
                                enumerate(hit_dist), key=operator.itemgetter(1))

                            if internal[mv_pos] in ["PeakInsideFeature", "FeatureInsidePeak"] and min_val != []:
                                Best_hits_tab[j][peak['id']] = hit_line[
                                    mv_pos] + "\n"
                                #logger.debug("\nBest Internal hit to be recorded: {}\n".format(hit_line[mv_pos]+"\n"))

                    else:  # if All_hits_tab[j][peak['id']] == "" :
                        continue

            # When no hits are valid for one query-> All_hits[q] stays <""> ->
            # Get them filled with NAs
            for a in range(len(queries)):
                if All_hits_tab[a][peak['id']] == "":
                    #log.debug("\nQuery {} didn't validate any hit ! All_hits will be filled in with NAs".format(a))
                    All_hits_tab[a][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                        'start'], str(peak['center']), peak['end'], NAsList_q, str(a) + "\n"]))
                if Best_hits_tab[a][peak['id']] == "":
                    #log.debug("\nQuery {} didn't validate any hit !Best hits will be filled in with NAs".format(a))
                    Best_hits_tab[a][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                        'start'], str(peak['center']), peak['end'], NAsList_q, str(a) + "\n"]))

            # end.for_hit
            if not has_hits or True not in has_hits:
                # Write the Non Overlaps in the first dict,so it is saved only once.
                # log.debug ("\nPeak has no hits ! All queries Tables will be
                # filled in with NAs\n") #only to [0]
                for j in range(len(queries)):
                    All_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                        'start'], str(peak['center']), peak['end'], NAsList_q, str(j) + "\n"]))
                    Best_hits_tab[j][peak['id']] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                        'start'], str(peak['center']), peak['end'], NAsList_q, str(j) + "\n"]))

            # > PRIORITY FLIPPING
            # Check for each Line in the Tabs if Query 1 = NA, when Pr= True
            # and replace with Secondary Query.
            if priority and len(queries) > 1:
                # empty if only 0 exists
                rest_q = [j for j in range(len(queries)) if j != 0]
                # ** All_hits_per_peak -> may have lots of hits, sep with \n

                isNA = list()
                for i in enumerate(queries):
                    if All_hits_tab[i[0]][peak['id']]:
                        isNA.append(All_hits_tab[i[0]][
                            peak['id']].split("\t")[9] == "NA")

                QnotNA = [pos for pos, val in enumerate(isNA) if val is False]
                Q_NA = [pos for pos, val in enumerate(isNA) if val is True]

                # All have Hit ,and Priority query
                if isNA[0] is False or not any(isNA):
                    for r in rest_q:
                        All_hits_tab[r][peak['id']] = Best_hits_tab[
                            r][peak['id']] = ""

                # 1st Query is NA, there are Sec.Queries. // any(QnotNA) = []
                # when isNA=[True] for one Q
                if isNA[0] is True and any(QnotNA):
                    # Queries with NA: map(lambda qna :
                    # All_hits_tab[qna][peak['id']], Q_NA)
                    repl_q = min(QnotNA)  # The query to be used instead of qO.
                    ##log.debug ("Priority Query hasn't given any hit, so it will be replaced by secondary Query's Hit: {} ".format (repl_q))
                    All_hits_tab[0][peak['id']] = Best_hits_tab[
                        0][peak['id']] = ""
                    ##log.debug ("\nHits from Secondary Q to replace priority query: \n{} ".format(All_hits_tab[repl_q][peak['id']] ))
                    rest_QnotNA = [qn for qn in QnotNA if qn != repl_q]
                    if any(rest_QnotNA):
                        for qr in rest_QnotNA:
                            All_hits_tab[qr][peak['id']] = Best_hits_tab[
                                qr][peak['id']] = ""
                    for qna in Q_NA:
                        All_hits_tab[qna][peak['id']] = Best_hits_tab[
                            qna][peak['id']] = ""

                if all(isNA):
                    #logg.debug("\nNo query has any Hit.No replacement of Priority Query possible-> NAs will be filled in the Output.")
                    TabInList_p = map(lambda l: All_hits_tab[l][
                        peak['id']], range(len(queries)))
                    ##log.debug("Hit lines for all queries are : {}".format(TabInList_p ))
                    # If all_hits_tab doesn't have all queries will have ""
                    TabInList_p = [Tab for Tab in TabInList_p if Tab != ""]

                    for j in enumerate(TabInList_p):
                        if j[1] == "":
                            TabInList_p[j[0]] = "\t".join(np.hstack([peak['name'], peak['chr'], peak[
                                'start'], str(peak['center']), peak['end'], NAsList_q, str(j[0]) + "\n"]))

                    All_hits_tab[0][
                        peak['id']] = ovls.merge_queries(TabInList_p)
                    Best_hits_tab[0][
                        peak['id']] = ovls.merge_queries(TabInList_p)
                    ##log.debug("\nQueries hits for this peak to be merged in the Q.col:{}".format(ovls.merge_queries(TabInList_p)) )
                    for r in rest_q:
                        All_hits_tab[r][peak['id']] = Best_hits_tab[
                            r][peak['id']] = ""

        All_combo = OrderedDict()  # Output peaks with same order as All_hits_tab
        mydict = All_hits_tab
        for k in mydict[0].iterkeys():
            All_combo[k] = [pid[k] for q, pid in mydict.items()]

        #  Best hits  #
        Best_combo = OrderedDict()
        mybestD = Best_hits_tab
        for k in mybestD[0].iterkeys():
            Best_combo[k] = [pid[k] for q, pid in mybestD.items()]

        def all_same(items):
            """Returns true if all items of a list are the same."""
            return all(x == items[0] for x in items)

        # > Merge hits of queries to have one best, if queries >1
        if len(queries) > 1 and not priority:
            BestBest_hits = OrderedDict()
            for k in Best_combo:
                # [  [] , [] , [] ]-> can be of same query, same distance
                records = map(lambda s: s.split("\n"), Best_combo[k])
                # split also internally each query's string to see if it
                # contains more >1 hits(when same distance, more >1 are conc.
                # to same query)
                spl_rec = map(lambda r: map(
                    lambda t: t if t != '' else None, r), records)
                recs = [x + "\n" for s in spl_rec for x in s if x != None]

                if len(recs) > 1:  # Only when more than two hits, and no NAs here
                    splitted_hits = map(
                        lambda h: recs[h].split("\t"), range(len(recs)))
                    # s= each hit line in string
                    splitted_hits = [s for s in splitted_hits if s != [""]]
                    featOfHit = map(lambda s: splitted_hits[s][
                        5], range(len(splitted_hits)))
                    startPos = map(lambda s: splitted_hits[s][
                        6], range(len(splitted_hits)))
                    endPos = map(lambda s: splitted_hits[s][
                        7], range(len(splitted_hits)))
                    Dist_hits = map(lambda s: float(splitted_hits[s][10]) if splitted_hits[s][
                        10] != "NA" else float("Inf"), range(len(splitted_hits)))  # 9th col= Distance
                    # Dist_hit = [Dist_hits[0] if all_same(Dist_hits) else
                    # Dist_hits]  #Either same dist or All NAs

                    # When All "NAs" for all queries-> keep only line from 1st
                    # query
                    NA_hits = map(lambda s: "NA" if splitted_hits[s][
                        10] == "NA" else None, range(len(splitted_hits)))
                    # If None means ALL queries have a feature
                    all_have_feat = all(x is None for x in NA_hits)

                    same_feat = (all_same(featOfHit) and all_same(
                        startPos) and all_same(endPos) and all_same(Dist_hits))

                    if len(splitted_hits) > 1:
                        if all_same(NA_hits):
                            # BestBest_hits[k] =  Best_combo[k][0]  #Keep only
                            # one of the hits wth NA
                            BestBest_hits[k] = ovls.merge_queries(
                                Best_combo[k])

                        if (all_have_feat and same_feat) or (not same_feat and all_same(Dist_hits)):
                            BestBest_hits[k] = ovls.merge_queries(
                                Best_combo[k])

                        if (all_have_feat) and not same_feat or (not all_same(NA_hits) and not all_have_feat):
                            # min_pos,min_v = min(enumerate(Dist_hits),
                            # key=operator.itemgetter(1)) ## If only one min in
                            # one pos
                            min_v = min(Dist_hits)
                            # retrieve the value of the list with [0],should be
                            # only 1 !
                            min_pos = [min_pos for min_pos, v in enumerate(Dist_hits) if v == min_v][
                                0]
                            # Keep to BB the pos with Min_Dist
                            BestBest_hits[k] = recs[min_pos]

                    elif len(splitted_hits) == 1:
                        BestBest_hits[k] = Best_combo[k]

        # > Write in file
        allhits_file = outdir + "allhits_part_" + prefix_pk + ".txt"

        try:
            ovls.write_partial_file(allhits_file, All_combo)
        except IOError:
            if not log is None:
                log.error("Unable to open file " + allhits_file + " for writing results!")
            sys.exit()

        finalhits_file = outdir + "finalhits_part_" + prefix_pk + ".txt"
        if len(queries) > 1 and not priority:
            besthits_file = outdir + "besthits_part_" + prefix_pk + ".txt"
            ovls.write_partial_file(besthits_file, Best_combo)
            ovls.write_partial_file(finalhits_file, BestBest_hits)
        else:
            ovls.write_partial_file(finalhits_file, Best_combo)
    return
