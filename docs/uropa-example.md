In this section several examples for the usage of the config file are presented. 

Example with two queries and difference in 'priority' 
----------------------------------------------------- 

More than one query can be given, keeping the same gtf and bed files, allowing for a combination of annotation in one run.    
If there are more queries, it is important to decide if they should be priorized. This can be done with the priority key in the config file.   
The following examples illustrate how this can be beneficial for the annotation.

The queries in the config file looks like the following.

This example is based on POLR2A peaks annotated with the Ensembl genome. 
Source files can be found here :[gtf and bed source files](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files)


`
{"queries": [{"feature":"gene", "distance":1000, "show.attributes":"gene_name"},     
			{"feature":"transcript", "distance":1000 }], 
 "priority" : "False",
 "gtf":"Homo_sapiens.GRCh37.75_chr.gtf" ,
 "bed":"ENCFF001VFA_GM12878_POLR2A_narrowPeaks.bed"
} `



+ If No priority is given ('priority'='False') 


	The above set of queries will allow UROPA to annotate peaks for genes and transcripts. As priority is False (default if no different value given),there is no feature priorized. 

	There can be three cases for the peak annotation: 

	* Case 1: No query gives any feature for annotating the peaks. 
	
	* Case 2: One query gives a feature but the other not. 
	
	* Case 3: Both queries validate features overlapping with the peaks.  



	The Tables [1] and [2] shown below, represent the AllHits and BestHits outputs of UROPA,respectively for the 3 cases. 
	
	For further details on the output tables format please visit [Output_tables](http://uropa.readthedocs.io/en/latest/output/)


	In the 'AllHits' all the features found within the given distance will be annotated for the peak, while 
	in the 'BestHits' only the annotation with the closest feature  per peak per query is displayed. 

 

	| peak_id | p_chr | p_start  | p_center | p_end    | feature  | feat_start| feat_end |feat_strand|distance | feat_pos   |genomic_location |feat_ovl_peak | peak_ovl_feat | gene_name| query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:----------------|:-------------|:--------------|:---------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         |NA       		  | NA      | NA          | NA   | 0     | 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         |NA               | NA      | NA          | NA   | 1     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |                 | 	    | 			  |      |       |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        |  3       |  start	    |FeatureInsidePeak|	0.01     | 1.0        |AC006483.1| 0 | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5566782 |	5567729  | -	    |  91	   |  start	    |FeatureInsidePeak|	0.09     | 1.0	      |ACTB	     | 1 |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5566787 |	5570232  | -		|  689	   |  center	|FeatureInsidePeak|	0.33	 | 1.0        |ACTB	     | 1 |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 |	5567817  | -	    |  3       |  start	    |FeatureInsidePeak|	0.01	 | 1.0	      |AC006483.1| 1 |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |          |            |          |   |
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | NA	        |	NA    |	  NA	 |   NA     |  NA      |	NA      | NA    	      |   NA     |	NA        |	 NA      | 0 |
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript |28832863 | 28836145 |   +      |  245	   |   end	    |FeatureInsidePeak|  0.37	 |  1.0	      | SNHG3	 | 1 | 
	| peak_10 | chr1  |	28832002 | 28836390 |28840778  | transcript	|28836589 |	28862538 |	 +	    |  199	   |   start	| overlapStart    |  0.48	 |  0.16	  |  RCC1	 | 1 |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |          |            |          |   |
	
	[Table 1: AllHits_table for two queries with priority false.] 


	'Peak_1' represents the **1st case**  where both queries validate no feature at all. In this case the peak is represented by 'NA' rows, for each query. 
	
	The **2nd case** is represented by 'peak_10', which has two annotations for the transcript feature but not the gene feature.       
	
	'Peak_6' is an example for the **3rd case** , with annotations for both queries. Transcripts (*ACTB*) are found by query 1 and a gene (*AC006483.1*) by query 0.


	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start|feat_end |feat_strand|distance | feat_pos   |genomic_location |feat_ovl_peak | peak_ovl_feat |gene_name| query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:----------------|:------------ |:--------------|:--------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         |NA       		  | NA       | NA         | NA       | 0     | 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         |NA               | NA       | NA         | NA       | 1     |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |          |            |          |       |         
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        |   3      |  start	    |FeatureInsidePeak|	0.01     | 1.0        |AC006483.1| 0     |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 |	5567817  | -	    |   3      |  start	    |FeatureInsidePeak|	0.01	 | 1.0	      |AC006483.1| 1     |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |          |            |          |       |
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 |   +      |   199	   |   start    |overlapStart     |  0.48	 |  0.16      | SNHG3	 |  1    |  
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |          |            |          |       |

	[Table 2: BestHits_table for two queries with priority false.]


	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start|feat_end |feat_strand|distance | feat_pos   |genomic_location |feat_ovl_peak | peak_ovl_feat | gene_name |query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:----------------|:-------------|:--------------|:----------|:-----| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       |   NA     | NA         | NA         	  |   NA         | NA            | NA        | 0,1  |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |              |               |           |      |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        |   3      |  start	    |FeatureInsidePeak|	    0.01     |  1.0          |AC006483.1 | 0    |
	| ...     |       |          |          |          |            |         |          |          |          |            |                 |              |               |           |      |    
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript	|28836589 |	28862538 |	+       |	199	   |  start	    |overlapStart     |	   0.48      | 	0.16         |SNHG3      |	1   |

	[Table 3: Merged_BestHits_table for two queries with priority false.]


	In Case 1,as reported in 'peak_1', the 'BestHits' table will be the same as the 'AllHits' because all queries give same annotation. This is why the 'Merged_BestHits' table was designed [Table 3]. Queries with same annotation are merged in one line, or the query with the 'closest' feature  among all queries is only given, providing a more compact illustration of the annotation.
	
	For the other 2 cases (peak_6, peak_10) the best feature is chosen according to the 'distance' measured from the peak center. For 'peak_6' the closest transcript and gene have both same distance = 3, so they are both reported in 'BestHits', but merged in one line at the 'Merged_BestHits'.
	
	For 'peak_10' the closest feature is the transcript with gene_name *RCC1*, so no merging was needed.


+ If Priority is considered ('priority'='True')

	If 'priority' is True, UROPA will annotate peaks with the **first feature given** in the set of queries. Unless genes are not found for a peak, 'transcripts' will then be searched and validated by the query’s parameters in order to be assigned to a peak. The example is based on the same three cases, explained above.
	That is why there will be no peak in the output tables annotated for both features at the same time. 
	Each peak is allowed to have the 1st feature or the 2nd, or the 3rd, etc.


	The first difference to the example without priority is that in 'AllHits' [Table 4], the peaks with no annotation for both queries are merged in one line and both queries are reported.    
	This is why the entries for peaks without any annotation will look the same in 'AllHits' and 'BestHits'.

	In the case of  'peak_6'  there is an annotation for the priorized query 0, so the other query is not further analyzed. 
	    
	For 'peak_10' there was no annotation identified for the query 0, but two 'transcripts' are found for query-1. The annotation with the closest distance, *SNHG3*  is displayed at the BestHits (Table 5).	
	

	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start| feat_end |feat_strand|distance | feat_pos   |genomic_location |feat_ovl_peak | peak_ovl_feat | gene_name |query |
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:----------------|:-------------| :-------------|:----------|:-----|
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | NA         	   |   NA         | NA            | NA        |0,1   |	
	| ...     |       |          |          |          |            |          |          |          |          |            |                 |              |               |           |      | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        |   3      |  start	 |FeatureInsidePeak|	0.01	  |     1.0       |AC006483.1 | 0    |  
	| ...     |       |          |          |          |            |          |          |          |          |            |                 |              |               |           |      | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28832863 | 28836145 |   +      |  245	    |   end	     |FeatureInsidePeak|    0.37	  |     1.0	      |   SNHG3	  | 1    |
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 |	  +      |	199	    |  start	 |   overlapStart  |	0.48      | 	0.16      |   SNHG3   |	1    | 
	| ...     |       |          |          |          |            |          |          |          |          |            |                 |              |               |           |      | 

	[Table 4: AllHits_table with two queries when priority='True']
	

	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start| feat_end |feat_strand |distance | feat_pos  | genomic_location | feat_ovl_peak | peak_ovl_feat | gene_name | query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:---------------|:--------------|:--------------|:---------|:------|
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | NA             |   NA     | NA       | NA       | 0,1   | 
	| ...     |       |          |          |          |            |          |          |          |          |            |                |          |          |          |       |   
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | start	     |FeatureInsidePeak|0.01	 |1.0	    |AC006483.1|  0    | 
	| ...     |       |          |          |          |            |          |          |          |          |            |                 |         |          |          |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 |	  +      |	199	    |  start	 |   overlapStart  | 0.48    | 	0.16    |   SNHG3  |  1    | 
	| ...     |       |          |          |          |            |          |          |          |          |            |                 |         |          |          |       |

	[Table 5: BestHits_table with two queries when priority is set 'True'.]
	

	**So, in the case of 'priority' = True, the features are mutually exclusive, and the queries are parsed for valid hits in an escalating priority.**        
	

Example for the 'feature.position' 
----------------------------------

UROPA allows flexibility of annotation for features. With the key 'feature.position' it is possible to decide from where the distance-to-the-peak should be calculated.    
The typical application is to calculate the distance from the TSS, respresented as 'start' of the feature,but with UROPA it is also possible to use the 'center' and 'end' of the feature in question. 

If no value is given, the distances from all three positions :  `'feature.position' =['start', 'center', 'end']`  to the peak center are calculated and,
if :  ` min(|feature.position - peak.center|) <= 'distance' ` , the feature is kept for annotation.                                                                                                     The position closer to the peak.center will be indicated in the output file in the column **'feat_pos'**.

This example is based on H3K4me1 peaks annotated with the Gencode genome. 
The source files can be found here: [gtf and bed source files](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files)

There are two queries with different 'feature.positions' for this example. 

` "queries": [ {"feature":"gene", "distance":5000, "feature.position": "start", "show.attributes":"gene_name", },       
		       {"feature": "gene","distance":5000, "feature.position": "center"} ]
  "priority" : "False"  `
		        

As displayed in the output below (Table 6), the peak could only be annotated for query 1 where 'feature.position' is set to 'center' and the measured distance is within the accepted cut-off value. 
The location of the gene and the peak of interest (highlighted in black colour) are shown in the Figure 1. The gene *BCL2L13*  is very large, that is why the measurement of distance from 'start' position couldn't return a valid annotation. 
											` feature.start – peak.center = |18111621-18161442| = 49 821 `


| peak_id | p_chr | p_start  | p_center   | p_end    | feature | feat_start | feat_end | feat_strand | distance | feat_pos | genomic_location | feat_ovl_peak | peak_ovl_feat | gene_name | query | 
|:--------|:------|:---------|:-----------|:---------|:--------|:---------|:---------|:---------|:---------|:----------|:-------------------|:--------------|:---------|:---------|:---------|
| ...     |       |          |            |          |         |          |          |          |          |           |                    |               |          |          |          |       
| peak71  | chr22 | 18161387 | 18161441.5 | 18161496 |   NA    | NA       | NA       | NA       | NA       | NA        | NA                 |     NA        |    NA    |    NA    |   0      |
| peak71  | chr22 | 18161387 | 18161441.5 | 18161496 |   gene  | 18111621 | 18213388 | +        | 1063     | center    | PeakInsideFeature  |     1.0       |    0.0   | BCL2L13  |   1      |
| ...     |       |          |            |          |         |          |          |          |          |           |                    |               |          |          |          | 
	
[Table 6: AllHits_table with annotation of a peak from two queries with different 'feature.position' and 'priority' = 'False'  ]


![peak71](img/chr22-18161287-18161496_peak71_h3k4me1_feature_pos.png)

Figure 1: From the histone mark H3K4me1, peak71(chr22:18161387-18161496) annotated with the gene *BCL2L13* from gencode, at a distance 1063bp from feature.center to peak.center

* BestHits_table will be same as All_hits_table for this peak because there is only one feature per query annotated.
* Merged_BestHits_table will only include the annotated peak given by query '1'.



**Note** : Similar cases of peaks being internally to the genomic region of a feature (and also features being internally to a peak region) 
can be well-annotated using a supplementary key in UROPA, the 'internals', which is explained in the section "Example for the 'internals' key".



Example for the 'direction' 
------------------------- 

In the following example the utility of the key 'direction' will be illustrated. It is optional but can be a very important 'player' for a more specialized annotation.                  

When the direction key is set to **'upstream'**, peaks will be annotated to a feature if the peak center is upstream of the feature and the distance from the 'feature.position' is smaller than the distance required in the config file. The same would be for **'downstream'**  where the location of the peak should be downstream of the gene (Figure 2).

So,the location of the peak is relative to the feature’s direction, and furthermore, the closest 'feature.position' is actually the 'start' when peak is upstream, while on the contrary, it is the 'end', if the peak is downstream.  This is why in the example the 'feature.position' will be used with default values.

*An overlap of the feature to the start or end of the peak is partially allowed, but the overlap should allow a clear evidence of the upstream or downstream location of the peak.*

![peak_upstream](img/peak_Upstream_Downstream_of_gene.png)

(found from : (https://www.geneprof.org/GeneProf/imgs/gp_fig_geneassoc.png)  )
Figure 2 : Location of a peak shown upstream of the TSS of a gene X. Respectively, if peak found on the right side it would be considered 'downstream' of the gene X



Let’s see now an example of an annotation with and without direction chosen, for the peak shown in Figure 3.
It is based on H3K4me1 peaks annotated with the Gencode genome, 
found here : [gtf and bed source files](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files)


![direction.key](img/chr1-1,403,500-1,408,500-01_h3k4me1_peaks.png)  

Figure 3: H3K4me1 peak annotated with the Gencode genome, the genomic location is chr1:1,403,500-1,408,500

    
The query is the following:       

`"queries": [{ "feature": "gene", "attribute":"gene_name", "distance":1000 }] `

The peak displayed in Figure 3 would be annotated for both genes as shown in the table below:


| peak_id   | p_chr | p_start  | p_center  | p_end    | feature | feat_start | feat_end | feat_strand | distance | feat_pos  | genomic_location | feat_ovl_peak | peak_ovl_feat | gene_name | query | 
|:----------|:------|:---------|:----------|:---------|:--------|:-----------|:---------|:---------|:----------- |:----------|:-----------------|:--------------|:---------|:----------|:---------|
|peak_21044 | chr1  | 1406116  | 1406250.5 | 1406385  | gene    |   1407143  |  1433228 |     +    |    892      | start     |     upstream	    |      0.0      |    0.0   |	ATAD3B |    0     |
|peak_21044 | chr1  | 1406116  | 1406250.5 | 1406385  | gene    |   1385069  |  1405538 |     +    |    712      | end	     |    downstream    |	   0.0      |    0.0   |	ATAD3C |    0     |

[Table 7 : AllHits_table for an H3K4me1-peak annotated with two genes according to the above config file ]


Due to the fact that no 'feature.position' was defined, the distance shown in the table is measured from the ` min(|[start,center,end] - peak.center|) `, 
as explained in "Example for the 'feature.position'" and the position having the minimum distance is given in the table : 'start' for  *ATAD3B*, 'end' for *ATAD3C* .


From All_hits_table we can infer the best annotation,too, which is this case, the gene *ATAD3C* , with distance 712 bp.  

But, let's see the differences when the 'direction' key is set. If only 'upstream' annotation is required :

`"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000, "direction":"upstream"}] `


In this case the peak will only be annotated for *ATAD3B* because it is located 'upstream' to it, while it is 'downstream' to the gene *ATAD3C* , so *ATAD3C*  it is not a valid feature, 
even though the distance is closer. 

**The direction is considered a priority parameter for the annotation, so only if direction is valid, the distance will then be validated, too.**

The location of a peak relative to the annotated feature can also be found at the column **'genomic_location'** even when 'direction' key is not given. This allows for an extra control of results, with or without filtering parameters.

**Note** : In some cases the 'upstream' direction will be matched with annotation of genomic_location = **'overlapStart'** , 
and respectively the 'downstream' direction will contain annotation with the genomic_location = **'overlapEnd'**, because a partial overlap with the feature is allowed when filtering for upstream/downstream peaks to features. 



So, globally, this example shows that more specific annotation can be useful for peaks like this one, in order to obtain a unique feature matching more specific requirements. 
There is interest in cases where for example, some genomic regions are known to be enriched in transcriptionally active promoters, and we would like to know to which features these regions are found upstream. Moreover, a ‘downstream’ direction could be useful for the targeted identification of miRNAs or 3’UTR-binding proteins.



Example for the 'internals' key
------------------------------------ 
This example is based on POLR2A peaks annotated with the Ensembl genome .Link for the source files can be found here:
[gtf and bed source files](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files)

By default this parameter is set to 'False'. With this setting, peaks are only annotated with features whose 'distance' is smaller than the defined one in the config.          

But there are cases where the genomic feature is larger than the set 'distance' and this case can lead to unannotated peaks, even if the peak is located inside the genomic feature interval (seen in the Example for the 'feature.position').     
Same the other way around, there exist very large peaks containing small features inside their interval. 
The 'internals' key was implemented exactly for these cases.   

So, peaks with a max distance from the feature are normally annotated with it, but **also** those who contain the feature internally, or are included in the features region. 
These internal features are the only ones allowed to be in a larger distance than the set 'distance'.

Especially, when ATACseq peaks are used for annotation with very small transcription factors, this option becomes very handy.          
The following configuration allows to search peaks internal to feature region and features internal to peak region :
`
"queries":[{"feature":"gene", "distance":500, "show.attributes":"gene_name", "internals" : "True"}]
`

The output will be for "peak_13":   
 
| p_chr   | p_start  | p_center | p_end    |feature |feat_start|feat_end |feat_strand|distance| feat_pos  | genomic_location  |feat_ovl_peak | peak_ovl_feat |gene_name |query| 
|:--------|:---------|:---------|:---------|:-------|:---------|:--------|:--------|:---------|:----------|:----------------- | :------------|:------------- |:---------|:----|
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27861203 | 27861669|   +     | 802      | start     |FeatureInsidePeak  |   0.07       |   1.0 	     | HIST1H2BO | 0  |
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27858093 | 27860884|   -     | 483      | start     |FeatureInsidePeak  |   0.43       |   1.0 	     | HIST1H3J  | 0  |
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27860477 | 27860963|   -     | 76       | end       |FeatureInsidePeak  |   0.08       |   1.0 	     | HIST1H2AM | 0  |

[ Table 8: AllHits_table internal feature example].

![internal.feature](img/chr6-27,857,165-27,863,637_internal_feature-01.png)

Figure 4: A polR2A-peak annotated with Ensembl, genomic location: chr6 : 27,858,000 - 27,863,000


As displayed in Table 7 there are three genes annotated for the peak which is shown in Figure 4.    

UROPA detects the internal-to-a-peak features or the internal-to-a-feature peaks and reports their 'genomic.location' in the output files. Even if the distances from feature.position to the peak center are larger than the 'distance' set, the features will be annotated to the corresponding peaks.
       
In the contrary case, where the key 'internals' is not activated ("False") and no feature.position is chosen,          
the peak would only be annotated with the two genes *HIST1H3J*  and *HIST1H2AM*  ,found in distance less than 500 bp(Table 8). 


| p_chr   | p_start  | p_center | p_end    |feature |feat_start|feat_end |feat_strand|distance| feat_pos  | genomic_location  |feat_ovl_peak | peak_ovl_feat |gene_name  |query| 
|:--------|:---------|:---------|:---------|:-------|:---------|:--------|:--------|:---------|:----------|:----------------- | :------------|:------------- |:----------|:----|
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27858093 | 27860884 |   -    |   483    | start     | FeatureInsidePeak |    0.43      |     1.0       | HIST1H3J  | 0   |
| chr6	  | 27857165 | 27860401 | 27863637 | gene   | 27860477 | 27860963 |   -	   |   76     | end       | FeatureInsidePeak |    0.08      |     1.0	     | HIST1H2AM | 0   |

[ Table 9 : AllHits_table with 'internals': 'False' for the peak_13 of polR2A ]


These examples make overally evident, that depending on the biological relevance, it can be very useful to utilize more flexible keys and allow better control of results. 


Combination of config keys
------------------------------

* **feature.position + direction** : If position is 'end' and the 'direction' given 'upstream', the features with upstream peaks will be annotated if the 'end' position is closer than the given 'distance'.

* **direction + internals** : If 'direction' is given for filtering and 'internals':'True', the features with 'upstream'/'downstream' peaks will be annotated, plus the internal-to-peak features or the internal-to-feature peaks will also be found in the results, with 'distance' further than the required.

* **feature.position + internals** : The feature.position will be used for measuring the closest distance to the peak.center and only the features in this cut-off will be annotated, except for  the internal-to-peak features and the internal-to-feature peaks that will be kept as supplementary annotations,irrespective of their distance.

* **filter.attribute + attribute.value** : The features for annotation will be filtered for the given 'attribute' key and only if they agree with the 'attribute.value' given, will they be associated to the peak. Both these values should be given to the config for the filtering to be done.

* **filter.attribute + show.attributes** : If the 'filter.attribute' is given, it is advised to also use the same key among others, at the 'show.attributes' so that filtered results are verified.
To be noted that 'show.attributes' can accept more than one attributes for displaying at the output tables.


**Note** : The combination is affecting results accordingly, when given in the same query. If used in different queries, they work independently,they are not considered as combined.


Used peak and annotation files 
------------------------------ 

Annotation:  

Ensembl database of the human genome, version hg19 (GRC37): [Ensembl genome](ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/)                      
Human Gencode genome, version hg19: [Gencode genome](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_19/) 

Narrow peak and signal files based on ChIP-seq of GM12878 immortalized cell line:  

[H3K4ME1](https://www.encodeproject.org/experiments/ENCSR000AKF/)   
[POLR2A](https://www.encodeproject.org/experiments/ENCSR000EAD/)     

**Note**: peak ids are manually added to make it easier to compare different tables or to combine tables with images. 


>> Still not sure how to use the config file? Please contact Maria Kondili(maria.kondili@mpi-bn.mpg.de)