In this section several examples for the usage of the config file are presented. 

Example with two queries and difference in 'priority' 
--------------------------------------------------- 
This example is based on POLR2A peaks annotated with the Ensembl genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
More than one query can be given, keeping the same gtf and bed files, allowing for a combination of annotation in one run.    
If there are more queries, it is important to decide if they should be priorized. This can be done with the priority key in the config file.   
The following examples illustrate how this can be beneficial for the annotation.

The queries in the config file looks like followed:  

```
				{"queries": [{"feature":"gene", "distance":1000, "attribute":"gene_name"},     
							{"feature":"transcript", "distance":1000 }], 
         		"priority" : "False",
         		"gtf":"Homo_sapiens.GRCh37.75_chr.gtf" ,
         		"bed":"ENCFF001VFA_GM12878_POLR2A_narrowPeaks.bed"
         		}
```

1. If No priority is given ('priority'='F')     
	The above set of queries will allow UROPA to annotate peaks for genes and transcripts. As priority is False (default if no different value given),there is no feature priorized. 

	There can be three cases for the peak annotation: 

	* Case 1: No query gives any feature for annotating the peaks. 
	
	* Case 2: One query gives a feature but the other not. 
	
	* Case 3: Both queries validate features overlapping with the peaks.  

	The Tables [1] and [2] shown below, represent the All_hits and Best_hits outputs of UROPA,respectively for the 3 cases. 
	
	In the 'All_hits' all the features found within the given distance will be annotated for the peak, while 
	in the 'Best_hits' only the annotation with the closest feature  per peak per query is displayed. 

 
	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | feat_start | feat_end    | feat_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 1     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567372 | 5569294  | -        | 448      | ACTB       | 1     | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567781 | 5570235  | -        | 39       | ACTB       | 1     | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 1     | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28832863| 28836145 | +        | 245      | SNHG3      | 1     | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 


	Table 1: All hits table for two queries with priority false. 


	'Peak_1' represents the first case where both queries validate no feature at all. In this case the peak is represented by 'NA' rows, for each query. 
	
	The 2nd case is represented by 'peak_10', which has two annotations for the transcript feature but not the gene feature.       
	
	'Peak_6' is an example for the last case, with annotations for both queries. Transcripts (*ACTB*) are found by query 1 and a gene (*AC006483.1*) by query 0.



	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start|feat_end |feat_strand|distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 1     |
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 1     | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     | 
	| ...     |       |          |          |          |      


	Table 2: Best hits table for two queries with priority false.


	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start|feat_end |feat_strand|distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0,1   |
	| ...     |       |          |          |          |            |         |          |          |          |            |       |
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0,1   |
	| ...     |       |          |          |          |            |         |          |          |          |            |       |
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     |


	Table 3: Merged best hits table for two queries with priority false.

	In Case 1,reported in 'peak_1', the 'Best_hits' table will be the same as the 'All_hits' because all queries give same annotation. This is why 'Merged_Best_Hits' table was designed [Table 3]. Queries with same annotation are merged in one line giving a more compact illustration of the annotation.
	For the other 2 cases (peak_6, peak_10) the best feature is chosen according to  'distance' measured from the peak center.For 'peak_6' the closest transcript and gene have both same distance = 3, so they are both reported in Best_hits, but merged in one line at the 'Merged_Best_hits'.
	For 'peak_10' the closest feature is the transcript with gene_name *RCC1*, so no merging was needed.


2. If Priority is considered ('priority'='True')     

	If 'priority' is True, UROPA will annotate peaks with the **first feature given** in the set of queries. Unless genes are not found for a peak, 'transcripts' will then be searched and validated by the query’s parameters in order to be assigned to a peak. The example is based on the same three cases, explained above.
	That is why there will be no peak in the output tables annotated for both features at the same time. 
	Each peak is allowed to have the 1st feature or the 2nd, or the 3rd, etc.


	The first difference to the example without priority is that in the All_hits [Table 4] the peaks with no annotation for both queries are merged in one line and both queries are reported.    
	This is why the entries for peaks without any annotation will look the same in All_hits and Best_hits.

	In the case of 'peak_6' there is an annotation for the priorized query 0, so the other query is not further analyzed. 
	Compare Tables 3 and 4.     
	For 'peak_10' there was no annotation identified for the query 0, but two for query 1, as displayed in Table 3. In this example, this is the only peak with a difference betweeen the two Tables: Here the two transripts are annotated because the query 0-gene was not found. As shown in Table 5 the annotation with the closest distance between these two is displayed at the Best hits, which is gene *RCC1*.	
	
	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | feat_start  | feat_end    | feat_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   |	
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28832863 | 28836145 | +        | 245      | SNHG3      | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 


	Table 4: All hits table with two queries when priority='True'
	

	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | feat_start| feat_end| feat_strand | distance | gene_name | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 


	Table 5: Best hits table with two queries when priority is set 'True'.
	

	**So, in the case of 'priority' = True, the features are mutually exclusive, and the queries are parsed for valid hits in an escalating priority.**        
	

Example for the 'feature.position' 
-------------------------------- 
UROPA allows flexibility of annotation for features. With the key 'feature.position' it is possible to decide from where the distance-to-the-peak should be calculated.    
The typical application is to calculate the distance from the TSS, respresented as 'start' of the feature,        
but with UROPA it is also possible to use the 'center' and 'end' of the feature in question. 

If no value is given, the distances from all three feature positions ('start', 'center', 'end') to the peak center are calculated. The minimum of all measured distances (|feature.position - peak.center|) is kept and if it is smaller than the indicated distance, the peak will be annotated for this feature. 

This example is based on H3K4me1 peaks annotated with the Gencode genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).

There are two queries with different feature.positions. 
```

"queries":  [{"feature":"gene", "attribute":"gene_name", "distance":[5000],"feature.position": "start"},       
		    {"feature": "gene", "feature.position": "center"}]

```

As displayed in the All_hits table(Table 5), the peak could only be annotated for query 1 with the 'feature.position' center. Visible in Figure 1, the gene *BCL2L13* is very large,   
that is why even if the peak is internal to the gene region, the start position of the feature 'gene' is far away to return a valid annotation.
```
(feature.start – peak.center = |18111621-18161442| = 49 821)    

```

| peak_id | p_chr | p_start  | p_center | p_end    | feature | feat_start  | feat_end    | feat_strand | distance | gene_name | Query | 
|:--------|:------|:---------|:---------|:---------|:--------|:---------|:---------|:---------|:---------|:----------|:------|
| ...     |       |          |          |          |         |          |          |          |          |           |       | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | NA      | NA       | NA       | NA       | NA       | NA        | 0     | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | gene    | 18111621 | 18213388 | +        | 1063     | BCL2L13   | 1     | 
| ...     |       |          |          |          |         |          |          |          |          |           |       | 

[Table 6: All hits table feature position example]


![peak71](img/chr22-18161287-18161496_peak71_h3k4me1_feature_pos.png)

Figure 1: H3K4me1 peak 71 annotated with the Ensembl genome, the genomic location is chr22:18161287-18161496.    


Example for the 'direction' 
------------------------- 
This example is based on H3K4me1 peaks annotated with the Gencode genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
In the following example the utility of the key 'direction' will be illustrated. It is optional but can be a very important 'player' for a more specialized annotation.             
The example is based on the peak displayed in Figure 2.     

When the direction key is set to 'upstream', peaks will be annotated to a feature if the peak center is upstream of the feature start-position and the distance from the start position is smaller than the indicated distance. The other way around for 'downstream'. This is why the direction is relative to the peak location. 
*It can also be thought of as the location of the peak depending on the feature’s direction.*       

*An overlap is partially allowed to the edges of the peak, but the overlap should allow a clear evidence*         
*of the upstream or downstream location of the peak from the feature, so there shouldn’t be an important overlap of the peak length*.

Let’s see now an example of an annotation with and without direction chosen, for the peak shown in Image 3.
![direction.key](img/chr1-1,403,500-1,408,500-01_h3k4me1_peaks.png) 

Figure 2: H3K4me1 peak annotated with the Gencode genome, the genomic location is chr1:1403500-1408500.
   
The query looks as the following:       
```

"queries": [{ "feature": "gene", "attribute":"gene_name", "distance":1000 }] 

```

The peak displayed in Figure 2 would be annotated for both genes: 

 * *ATAD3C* with a distance of 712.5 bp and
 * *ATAD3B* with a distance of 892.5 bp. 

Due to the fact that no 'feature.position' was defined, the distance calculated was chosen after a comparison of distances to find the minimum to the peak.center.

So for *ATAD3C* the distance is measured from the 'end' and the distance for *ATAD3B* is measured from the 'start',as shown in the output table in column 'feature.position'. 

The best annotation in this case would be the gene *ATAD3C*.  

But, more specific annotation can be useful for some peaks like this one, in order to obtain a unique and precise annotation. 
For example, if some genomic regions are known to be enriched in transcriptionally active promoters, we would be interested to know on which features these regions are found upstream.   
Also,‘downstream’ direction could be useful for the targeted identification of miRNAs or 3’UTR-binding proteins.
It is then possible in UROPA via the config file to add the parameter 'direction': 'upstream' to the query.
```

"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000, "direction":"upstream"}]           

```
In this case the peak will only be annotated for *ATAD3B*. Depending on the biological relevance, it can be very useful to utilize more flexible keys. 



Example for the 'internals' key
------------------------------------
This example is based on POLR2A peaks annotated with the Ensembl genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
By default this feature is false. With this attidue only such peaks are annotated whose distance is smaller than the definded one.          
But there are cases where the genomic feature is larger as the set distance, this can lead to unannotated peaks, even if the peak is inside the genomic feature.     
Same the other way around, very large peaks and small features. For those cases, the internal key was implemented.            
To say usually peaks with a max distance should be annotated, but also those who are internal, or include the feature.      
Especially, when ATACseq peaks are used for annotating them with very small transcription factors, this option becomes very handy.          
The following configuration allows for searching peaks internal features and featurs internal of peaks:
```

"queries":[{"feature":"gene", "distance":1000, "attribute":"gene_name", "internals" : "True"}]

```

The output will be:   
 
| p_chr   | p_start  | p_center | p_end    |feature |feat_start|feat_end |feat_strand|distance| feat_pos  | genomic_location  |feat_ovl_peak | peak_ovl_feat |gene_name | Query  | 
|:--------|:---------|:---------|:---------|:-------|:---------|:--------|:--------|:---------|:----------|:----------------- | :------------|:------------- |:---------|:-------|
| ...     |          |          |          |        |          |         |         |          |           |             	  |              | 	             |          |        |
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27861203 | 27861669| +       | 802      | start     |FeatureInsidePeak  | 0.07         | 1.0 	         |HIST1H2BO |   0    |
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27858093 | 27860884| -       | 483      | start     |FeatureInsidePeak  | 0.43         | 1.0 	         |HIST1H3J  |   0    |
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27860477 | 27860963| -       | 76       | end       |FeatureInsidePeak  | 0.08         | 1.0 	         |HIST1H2AM |   0    |
| ...     |          |          |          |        |          |         |         |          |           |                   |              |               |          |        |

[ Table 7: All hits table internal feature example].

![internal.feature](img/chr6-27,857,165-27,863,637_internal_feature-01.png)

Figure 3: H3K4me1 peaks annotated with Ensembl, genomic location: chr6-27,857,165-27,863,637

As displayed in Table 5 there are three genes annotated for the peak which is shown in Figure 3.    

UROPA detects the internal-to-a-peak features or the internal-to-a-feature peaks and reports their 'genomic.location' in the output files. Even if the distances from feature.position to the peak center  are larger than the 'distance' set, the features will be annotated to the corresponding peaks.
       
In the contrary case, where the key 'internals' is not activated (by default "False") and no feature.position is chosen,          
the peak would only be annotated for *HIST1H3J*  with a distance of 483 bp. 


| p_chr   | p_start  | p_center | p_end    | feature| feat_start  | feat_end   | feat_strand| distance | gene_name| Query   | 
|:--------|:---------|:---------|:---------|:-------|:---------|:--------|:--------|:---------|:----------|:-------| 
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27858093 | 27860884| -       | 483        | HIST1H3J  | 0      |


Used peak and annotation files 
------------------------------ 
Annotation:  
Ensembl database of the human genome, version hg19 (GRC37): [Ensembl genome](ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/)                      
Human Gencode genome, version hg19: [Gencode genome](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_19/) 

Narrow peak and signal files based on ChIP-seq of GM12878 immortalized cell line:  
[H3K4ME1](https://www.encodeproject.org/experiments/ENCSR000AKF/)   
[POLR2A](https://www.encodeproject.org/experiments/ENCSR000EAD/)     
**Note**: peak ids are manually added to make it easier to compare different tables or to combine tables with images. 

Still not sure how to use the config file? Please contact Maria Kondili(maria.kondili@mpi-bn.mpg.de)