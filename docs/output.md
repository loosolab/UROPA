UROPA provides many output files, each providing a valuable information in either a more extended or a more condense way, to cover all needs and be useful for further downstream analysis.

The different outputs will be explained thoroughly below.

#Output Files
**All_hits_table**  : The basic output table giving for each peak at least a hit which is valid according to the query's parameters. If more than one features are valid, all are shown in this table.

**Best_hits_table** : The table which can be the most useful for peak annotation.For each peak only one feature is assigned,the closest one.If more queries are given and each query validates different features, one feature per query is assigned to the peak.

**Merged_Best_hits_table** : The table that summarizes the Best_hits_table by chosing one feature for each peak in case more queries are given and each query validates one feature.The closest feature from all queries should be shown here.

**Reformatted_Besthits_table** : This table is created by an optional flag in the command line when running UROPA(-r).It creates a compact table with all hits per peak per query in one line, separated by semicolon, so one can have all the annotated features per peak at once.It is therefore created only when multiple queries are given.

**Results_Summary_Visualisation.pdf** : In this document one can obtain graphical information of the peak annotation run by UROPA,depending on the configuration file requirements and the output tables created(Best_hits_table or Merged_Best_hits_table are used).



#Output columns explanation

The four output tables mentioned above contain many informative columns about the peak annotation performed. The headers and content are explained below.

**feature, feature_start, feature_end, feature_strand** : The information of the genomic feature that annotates the peak, as extracted by the gtf file.

**distance** : The distance measured as following: abs(peak.center-feature.position).If no feature.position given,then the minimum of 3 distances from each feature.position{start,center,end} to peak.center is chosen.

**feat_pos**: The position of the genomic feature annotated,having the minimum distance to the peak.center.If 'feature.position' given in config only this will be shown.

**genomic_location**: The position of the peak relative to the annotated feature direction.(i.e upstream = peak located upstream of the gene).

**feat_ovl_peak**: When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / peak.length) shows percentage of peak covered by the feature.(i.e 1.0 = 100% of peak covered, peak is internal.

**peak_ovl_feat**: When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / feature.length) shows percentage of feature covered by the peak.(i.e 1.0 = 100% of feature covered, feature is internal.)

**gene_name, gene_id, gene_type** : Attributes that have been given in the key 'show.atttributes' will be shown here and their values extracted by the gtf will be displayed for each feature.If 'filter.attribute' contains same attribute keys, this column helps confirming the filtering.
	**Important Note** : Make sure to give any attributes for display in the output-if existant in the 9th column of the gtf - otherwise the annotated peaks will be reported 
	without any information of the assigned features.

**query**: The query that validates with its given parameters the feature to be assigned to the peak.If only one query given, column will always display '0',the first query.



#Summary Vizualisation

For every run there is also a summary output, vizualising the results for a global overview of the final annotation. Within this document one can find : 

---> Graphs based on the 'Best Hits' output:

* A pairwise comparison among all queries is evaluated within a venn diagram, when more than one query is given in the config file. 
* A distribution of the distances per feature per query are displayed in a histogram.
* A pie chart illustrating the genomic location of the peaks per annotated feature.
* A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation.

---> Graphs based on the 'Merged Best Hits' output:

* A density plot displaying the distance per feature per query. 
* A pie chart illustrating the genomic locations of the peaks per annotated feature.
* A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation.
