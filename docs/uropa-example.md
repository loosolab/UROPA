In this section several examples for the usage of the config file are presented. 

Example with two queries and difference in priority 
--------------------------------------------------- 
This example is based on POLR2A peaks annotated with the Ensembl genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
More than one query can be given, keeping the same gtf and bed files, allowing for a combination of annotation in one run.    
If there are more queries, it is important to decide if they should be priorized. This can be done with the priority key in the config file.   
The following examples illustrate how this can be beneficial for the annotation.    
The queries in the config file looks like followed:  
"queries": [{"feature":"gene", "distance":1000, "attribute":"gene_name"},     
{"feature":"transcript", "distance":1000}],          
The only difference between 1. and 2. is the priority key:                  

1. No priority is given ('priority'='F')     
	The above set of queries will allow UROPA to annotate peaks for genes and transcripts. As priority is False (default if no different value given),there is no feature priorized.            
	There can be three cases for the peak annotation: 
	Case 1: No query gives any feature for annotating the peaks. 
	Case 2: One query gives a feature but the other not. 
	Case 3: Both queries validate features overlapping with the peaks.  

	The Tables [1], and [2], shown below, represent the All_hits and Best_hits outputs of UROPA,respectively for the 3 cases. 
	
	In the 'All_hits' all the features found within the given distance will be annotated for the peak,while 
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
	Those are merged in the Best_hits Table 2, with Query information 0,1.       
	
	The second case is represented by 'peak_10', which has an annotation for the transcript feature but not the gene feature.       
	There are three entries,two with the annotation based on query 1 and one NA row, because no annotation with query 0 was identified.     
	
	'Peak_6' is an example for the last case, with annotations for both queries. Transcripts(*ACTB*) are found by query 1 and a gene(*AC006483.1*) by query 0.



	| peak_id | p_chr | p_start  | p_center | p_end    | feature    |feat_start|feat_end |feat_strand|distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 1     |
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 1     | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     | 
	| ...     |       |          |          |          |            |         |          |          |          |            |       | 

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


2. Priority is considered ('priority'='T')     

	The set of queries will allow UROPA to annotate peaks for genes. Only if there is no gene detected with the given parameters,     
	UROPA will assign to the peaks the feature transcript for annotation. The feature gene is priorized.The example above is based on the same three cases.
	That is why there is no peak in the output tables annotated for both features. Each peak is allowed to have either one feature or the other.


	The first difference to the example above is that already in the All_hits Table 3 those peaks with no annotation for both queries are merged.    
	That is why the entries for peaks without any annotation will look the same in All_hits and Best_hits, compare Best_hits Table 4.     
	Because for peak_6 there is already an annotation for the priorized query 0, the other query is not further analyzed, compare Tables 3, and 4.     
	For peak_10 there was no annotation identified for the query 0, but two for query 1, as displayed in Table 3. In this example, this is the only peak    
	with a difference betweeen the two Tables, in Table 4 only the annotation with the closest distance is displayed, which is gene *RCC1*.	
	
	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | feat_start  | feat_end    | feat_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   |	
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28832863 | 28836145 | +        | 245      | SNHG3      | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 

	Table 3: All hits table two queries with priority true
	
	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | feat_start  | feat_end    | feat_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 

	Table 4: Best hits table two queries with priority true
	
	*So, in the case of 'priority' =True, the features are mutually exclusive, and the rest of the queries should be parsed for valid hits in an escalating-priority, too.*        
	
Example for the feature position 
-------------------------------- 
UROPA allows flexibility of annotation for features. With the 'feature.position' key it is possible to decide from where the distance to the peak should be calculated.    
The typical application is to calculate the distance from the TSS, respresented as 'start' of the feature,        
but with UROPA it is also possible to use the 'center' and 'end' of the analyzed feature. If no value is given, the distance from all three feature positions (['start', 'center', 'end'])     
are calculated, and if one of them is smaller than the indicated distance, the peak will be annotated for this feature.   
This example is based on H3K4me1 peaks annotated with the Gencode genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
There are two queries with different feature.positions and if peaks are internal is not taken into account:   
"queries":  [{"feature":"gene", "attribute":"gene_name", "distance":[5000],"feature.position": "start"},       
		    {"feature": "gene", "feature.position": "center"}],
"internal"="False"

As displayed in the All_hits Table 5, the peak could only be annotated for query 1 with the 'feature.position' center. Visible in Figure 1, the gene *BCL2L13* is very large,   
that is why even if the peak is internal of the gene, the start position of the feature gene is to far away (feature.start – peak.center = \|18111621-18161442\| = 49 821)    
to return a valid annotation. 

| peak_id | p_chr | p_start  | p_center | p_end    | feature | feat_start  | feat_end    | feat_strand | distance | gene_name | Query | 
|:--------|:------|:---------|:---------|:---------|:--------|:---------|:---------|:---------|:---------|:----------|:------|
| ...     |       |          |          |          |         |          |          |          |          |           |       | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | NA      | NA       | NA       | NA       | NA       | NA        | 0     | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | gene    | 18111621 | 18213388 | +        | 1063     | BCL2L13   | 1     | 
| ...     |       |          |          |          |         |          |          |          |          |           |       | 

Table 5: All hits table feature position example

![peak71](img/chr22-18161287-18161496_peak71_h3k4me1_feature_pos.png)

Figure 1: H3K4me1 peak 71 annotated with the Ensembl genome, the genomic location is chr22:18161287-18161496.    

Example for the direction 
------------------------- 
This example is based on H3K4me1 peaks annotated with the Gencode genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
In the following example the utility of the key 'direction' will be illustrated. It is optional but can be a very important 'player' for a more specialized annotation.             
The example is based on the peak displayed in Figure 2.     
*It can also be thought of as the location of the peak depending on the feature’s direction.* 

When the direction key is set to 'upstream', peaks will be annotated to a feature if the peak center is upstream of the feature start postition and             
the distance from the start position is smaller than the indicated distance. The other way around for 'downstream'. This is why the direction is relative to the peak location.      
*An overlap is partially allowed to the edges of the peak, but the overlap should allow a clear evidence*         
*of the upstream or downstream location of the peak from the feature, so there shouldn’t be an important overlap of the peak length*.

Let’s see now an example of an annotation with and without direction chosen, for the peak shown in Image 3.
![direction.key](img/chr1-1,403,500-1,408,500-01_h3k4me1_peaks.png) 

Figure 2: H3K4me1 peak annotated with the Gencode genome, the genomic location is chr1:1403500-1408500.
   
The query looked as followed:         
"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000}]        
The peak displayed in Figure 2 would be annotated for both genes: 
*ATAD3C* with a distance of 712.5 bp and *ATAD3B* with a distance of 892.5 bp. Due to that no feature.position was defined, the distance calculated for *ATAD3C*        
is the distance from the gene end and the distance for *ATAD3B* the distance to the gene start. The best annotation in this case would than be the gene *ATAD3C*.    
More specific annotation can be usefull for some peaks. For example, if the peaks are known to be enriched in transcriptionally active promotors.   
It is possible to add the direction key with 'upstream' to the querie:          
"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000, "direction":"upstream"}]           
In this case the peak will only be annotated for *ATAD3B*. Depending on the biologically relevance, it can be very usefull to utilize the accessible keys. 


Example for the internal.feature key
------------------------------------
This example is based on POLR2A peaks annotated with the Ensembl genome ([further details])[http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files]).
By default this feature is false. With this attidue only such peaks are annotated whose distance is smaller than the definded one.          
But there are cases where the genomic feature is larger as the set distance, this can lead to unannotated peaks, even if the peak is inside the genomic feature.     
Same the other way around, very large peaks and small features. For those cases, the internal key was implemented.            
To say usually peaks with a max distance should be annotated, but also those who are internal, or include the feature.      
Especially, when ATACseq peaks are used for annotating them with very small transcription factors, this option becomes very handy.          
The following configuration allows for searching peaks internal features and featurs internal of peaks:
"queries":[{"feature":"gene", "distance":1000, "attribute":"gene_name"}],
"internal.features": "True"
The output would be:   
 
| p_chr   | p_start  | p_center | p_end    | feature| feat_start  | feat_end   | feat_strand| distance | gene_name| Query   | 
|:--------|:---------|:---------|:---------|:-------|:---------|:--------|:--------|:---------|:----------|:-------| 
| ...     |          |          |          |        |          |         |         |          |           |        | 
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27861203 | 27861669| +       | 0        | HIST1H2BO | 0      | 
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27858093 | 27860884| -       | 0        | HIST1H3J  | 0      | 
| chr6    | 27857165 | 27860401 | 27863637 | gene   | 27860477 | 27860963| -       | 0        | HIST1H2AM | 0      | 
| ...     |          |          |          |        |          |         |         |          |           |        | 

Table 6: All hits table internal feature example

![internal.feature](img/chr6-27,857,165-27,863,637_internal_feature-01.png)

Figure 3: H3K4me1 peaks annotated with Ensembl, genomic location: chr6-27,857,165-27,863,637

As displayed in Table 5 there are three genes annotated for the peak which is shown in Figure 3.    
Their distance is reportet as 0, because UROPA detects the internal features by their position even when their distances from the peak.center       
to all feature positions (no specific chosen in the configuration) would be larger than set.        
In the contrary case, where the option 'internal.feature' is not activated and no feature.position is chosen,          
the peak would only be annotated for *HIST1H3J* with a distance of 483 bp. 

Used peak and annotation files 
------------------------------ 
Annotation:  
Ensembl database of the human genome, version hg19 (GRC37): [Ensembl genome](ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/)                      
Human Gencode genome, version hg19: [Gencode genome](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_19/) 

Narrow peak and signal files based on ChIP-seq of GM12878 immortalized cell line:  
[H3K4ME1](https://www.encodeproject.org/experiments/ENCSR000AKF/)   
[POLR2A](https://www.encodeproject.org/experiments/ENCSR000EAD/)     
**Note**: peak ids are manually added to make it easier to compare different tables or to combind tables with images. 

Still not sure how to use the config file? Please contact Maria Kondili(maria.kondili@mpi-bn.mpg.de)