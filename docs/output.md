UROPA provides many output files, each providing valuable information in either a more extended or a more condense way, to cover all needs and be useful for further analyses.

The different outputs will be explained thoroughly below.

#Output Files
* **Uropa_AllHits**  : The basic output table giving for each peak all valid annotations and additionally NA rows for invalid annotations.

* **Uropa_FinalHits** : The table which can be the most useful for peak annotation.It provides the best-selected feature according to the config criteria for annotating each peak. The closest distance is the basic parameter for the selection. It also summarizes the 'BestperQuery_Hits' by chosing the closest feature for each peak in case more queries are given and each query validates a different feature.

* **Uropa_BestperQuery_Hits** : Only if more than one query is specified: Best valid annotation per query for each peak.

* **Uropa_Reformatted_HitsperPeak** : Only if more than one query is specified and the *-r* parameter is used: Compact table with best per query annotation in one row. 

* **Uropa_Summary.pdf** : Only if the *-s* parameter is used: Graphical information of the peak annotation run by UROPA.

**Note** : The output files will be named additionally by the output directory name where they are located, for convenience in further use and transfer of files.
Example  : ChIPannot/Uropa_AllHits_*ChIPannot*.txt


#Output columns explanation

The four output tables mentioned above contain many informative columns about the peak annotation performed. The headers and content of tables are explained here :
**peak_id, peak_start, peak_center, peak_end** : Peak information with id if available, otherwise a peak id in chr:start-end scheme will be created.

**feature, feat_start, feat_end, feat_strand** : The information of the genomic feature that annotates the peak, as extracted by the gtf file.

**feat_anchor**: The position of the genomic feature annotated, having the minimum distance to the peak.center. If 'feature.anchor' given in config only this will be shown.

**distance** : The distance measured as following: _abs(peak_center-feature_anchor)_. If no feature.anchor is given, the minimum of all feature.anchor {start,center,end} to peak_center is chosen.

**genomic_location**: The position of the peak relative to the annotated feature direction (e.g. upstream = peak located upstream of the gene, see Figure 2 in [Usage Examples](http://uropa.readthedocs.io/en/latest/uropa-example/#example-2-direction-key)).

**feat_ovl_peak**: When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / peak length) shows percentage of peak covered by the feature.(i.e 1.0 = 100% of peak covered, peak is internal.

**peak_ovl_feat**: When peak and feature overlap(i.e genomic_location = FeatureInsidePeak), Ratio(overlapping region / feature length) shows percentage of feature covered by the peak.(i.e 1.0 = 100% of feature covered, feature is internal.)

**gene_name, gene_id, gene_type** : Attributes that have been given in the key 'show.atttributes' will be shown here and their values extracted by the gtf will be displayed for each feature.If 'filter.attribute' contains same attribute keys, this column helps confirming the filtering.
**Important Note** : Make sure to give any attributes for display in the output-if existant in the 9th column of the gtf - otherwise the annotated peaks will be reported 
without any information of the assigned features.

**query**: The query that validates with its given parameters the feature to be assigned to the peak.If only one query given, column will always display '0',the first query.


#Output files (one query)
UROPA annotation with one query results in two output tables. Those are the Uropa_AllHits and Uropa_FinalHits. 
With a configuration as followed, a cut out of the AllHits would look as in Table 1, and a cut out of the FinalHits as displayed in Table 2. Peak and annotation files are further described [here](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files). 

```json
{
"queries":[
		{"feature":"gene", "distance":10000, "feature.anchor":"start", "internals":"True", "filter.attribute":"gene_type",  
		"attribute.value":"protein_coding","show.attributes":["gene_name","gene_type"]}], 
 "priority" : "False",
 "gtf":"gencode.v19.annotation.gtf" ,
 "bed":"ENCFF001VFA.bed"
}
```

![table1](img/output-formats-01.png)	
_Table 1: AllHits for one query_

![table2](img/output-formats-02.png)	
_Table 2: FinalHits for one query_

As displayed in Table 1, peak_22 has two valid annotations, but only the best of those is presented in the FinalHits as displayed in Table2.
The peaks peak_355 and peak_356 have either no valid annotation or only one valid annotation, thus they stay the same in both files. 

#Output files (multiple queries)
UROPA annotation with multiple queries result in at least three output tables. Those are the Uropa_AllHits, Uropa_FinalHits, and Uropa_BestperQuery_Hits. If the *-r* parameter is added in the command line call, there will the additional output Uropa_Reformatted_HitsperPeak file.
With a configuration as followed, a cut out of all generated output files will look as in Table 3 to 6 and Figure 1. Peak and annotation files are further discribed [here](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files). 
```json
"queries":[
		{"feature":"gene", "distance":10000, "feature.anchor":"start", "internals":"True", 
			"filter.attribute":"gene_type",  "attribute.value":"protein_coding",
			"show.attributes":["gene_name","gene_type"]},
		{"feature":"gene", "distance":10000, "feature.anchor":"start", "internals":"True", 
			"filter.attribute":"gene_type",  "attribute.value":"lincRNA"},
		{"feature":"gene", "distance":10000, "feature.anchor":"start", "internals":"True", 
			"filter.attribute":"gene_type",  "attribute.value":"misc_RNA"},
          ],
"priority" : "False",
"gtf": "gencode.v19.annotation.gtf",
"bed": "ENCFF001VFA.peaks.bed"
}
```

![table3](img/output-formats-03.png)	
_Table 3: AllHits for multiple queries_

![table4](img/output-formats-04.png)	
_Table 4: FinalHits for mulitple queries_

![table5](img/output-formats-05.png)	
_Table 5: Uropa_BestperQuery_Hits for multiple queries_

![table6](img/output-formats-06.png)	
_Table 6.1: Uropa_Reformatted_HitsperPeak for multiple queries part one_

![table6](img/output-formats-07.png)	
_Table 6.2: Uropa_Reformatted_HitsperPeak for multiple queries part two_

#Summary Vizualisation

For every run there is also a summary output, vizualising the results for a global overview of the final annotation. Within this document one can find : 

A summery of the UROPA run: Used peak and annotation files, number of peaks and number of annotated peaks, specified queries, value of priority flag (Fig. 1A). If not all queries annotated peaks, this is also mentioned.

---> Graphs based on the 'FinalHits' output:

* A density plot displaying the distance per feature across all queries (Fig. 1B). 
* A pie chart illustrating the genomic locations of the peaks per annotated feature (Fig. 1C).
* A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation (not illustrated due to one feature in this example).

**Figure 1 A-C would be the summary for the first UROPA run with only one query***

---> Graphs based on the 'BestperQuery_Hits' output:

* A distribution of the distances per feature per query are displayed in a histogram (Figure 1D).
* A pie chart illustrating the genomic locations of the peaks per annotated feature (not illustrated).
* A pairwise comparison among all queries is evaluated within a venn diagram, when more than one query is given in the config file (One pairwise comparison displayed in Figure 1E). 
* Chow Ruskey plot with comparison across all defined queries (for three to five annotation queries)(Figure 1F).

![summary](img/output-formats-summary.png)	
_Figure 1: Summary Example for queries as described above: (A) Summery of specified queries, used annotation and peak files, and how many peaks were present and annotated, (B) Distance density for all features based on FinalHits, (C) Pie Chart representing genomic location for each feature across FinalHits, (D) Distance per query per feature across BestperQuery_Hits, (E) Pairwise comparison across all queries displayed in Venn diagramms, (F) Chow Ruskey plot to compare all queries._




