In this section several examples for the usage of the config file are presented. 

Example with two queries and difference in priority 
--------------------------------------------------- 
This example is based on POLR2A peaks annotated with the Ensembl genome ([further details])[Used peak and annotation files])
In this example POLR2A peaks from UCSC (processed data accession ENCFF001VFA) were annotated with the Ensembl reference genome release 75 ([further details](#"Used peak and annotation files")).
More than one query can be given keeping the same gtf and bed files allowing for a combination of annotation in one run.    
If there are more queries, it is important to decide if they should be priorized. This can be set with the priority key in the config file.   
The following examples illustrate how this can be beneficial for the annotation.    
The queries in the config file looks like followed:  
"queries": [{"feature":"gene", "distance":1000, "attribute":"gene_name"},     
{"feature":"transcript", "distance":1000}],          
The only difference between 1. and 2. is the priority key:                  

1. No priority is given ('priority'='F')     
The set of queries will allow UROPA to search for genes and transcripts for each peak. As priority is false, there is no feature priorized.            
There can be three cases for the peak annotation: Either a peak cannot be annotated for any query, it can be annotated with one of both queries,     
or it could be annotated with both queries.  
In Table 4 there are peaks for all cases represented.     
The peak_1 represents the first case, both queries have no hit at all. The second case is represented by peak_10,       
which has an annotation for the transcript feature but not the gene feature. The peak_6 is an example for the last case, with annotations for both queries.   
For all three cases there are peaks in the following All_hits_table:  
 
| peak_id | p_chr | p_start  | p_center | p_end    | feature    | f_start | f_end    | f_strand | distance | gene_name  | Query | 
|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 1     | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567372 | 5569294  | -        | 448      | ACTB       | 0     | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567781 | 5570235  | -        | 39       | ACTB       | 0     | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0     | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        | 3        | AC006483.1 | 1     | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 
| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     | 
| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | NA         | NA      | NA       | NA       | NA       | NA         | 0     | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 

Table 4: All hits table two queries with priority false    

The Best_hits_table merges peaks without any annotation. If there is only one annotation for all queries, only this will be displayed,    
for peaks with more annotations, the best for each query will be present, as shown in the following table:

| peak_id | p_chr | p_start  | p_center | p_end    | feature    | f_start | f_end    | f_strand | distance | gene_name  | Query | 
|:--------|:------|:---------|:---------|:---------|:-----------|:--------|:---------|:---------|:---------|:-----------|:------| 
| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA      | NA       | NA       | NA       | NA         | 0,1   | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | transcript | 5567734 | 5567817  | -        | 3        | AC006483.1 | 0     | 
| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734 | 5567817  | -        | 3        | AC006483.1 | 1     | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 
| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589| 28862538 | +        | 199      | RCC1       | 1     | 
| ...     |       |          |          |          |            |         |          |          |          |            |       | 

Table 5: Best hits table two queries with priority false

**TODO** Merged: Why isnt feature merged but query is? --> both features in feature column?? why only first?    
What happens if different features have different best hits?      
In the Merged_Best_hits table, best hits will be merged if the result for all queries are the same.                   
*The Merged_Best_hit table can illustrate more 'economically' the feature with the closest distance among the best ones, and the query from which it was found.*    
*However, as they both have the same distance in this example the merging is still done, keeping one of the features with this distance and reporting both queries.*    
*So, when there is a merging of queries for a peak in the Merged_Best_hits table, it originates from the multiple hits overlapping with the peak in same distance,*     
*and only the first feature will be shown.*
*Therefore, as it has been shown in the above example, a multiple-query annotation can allow a wider annotation flexibility and exploration of the data.*  


| peak_id | p_chr | p_start | p_center | p_end   | feature    | f_start | f_end   | f_strand | distance | gene_name  | Query | 
|:--------|:------|:--------|:---------|:--------|:-----------|:--------|:--------|:---------|:---------|:-----------|:------| 
| ...     |       |         |          |         |            |         |         |          |          |            |       | 
| peak_6  | chr7  | 5562617 | 5567820  | 5573023 | gene       | 5567734 | 5567817 | -        | 3        | AC006483.1 | 0,1   | 
| ...     |       |         |          |         |            |         |         |          |          |            |       | 


2. Priority is considered (priority=T)     
The set of queries will allow UROPA to search for genes for each peak, unless a peak can not be annotated for the feature gene,    
UROPA tries to annotate this peak for the feature transcript. The feature gene is priorized.   
That is why there will not be a peak in the output tables, that is annotated for both features. The All_hits table looks as followed:     

	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | f_start  | f_end    | f_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28832863 | 28836145 | +        | 245      | SNHG3      | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 

	In the All_hits table shown above, we observe the same three cases that were explained before, in a query where the gene is the priority feature to be annotated.     
	In case a gene is not found, the transcript is searched. If no transcript is overlapping with the peak then the peak will be reported with both     
	the queries that were used for the research of annotation, as shown in the example of peak_1.     
	If a gene is found, then, it will be the only one annotating the peak (peak_6).     
	Finally, when transcripts are found instead of genes, they will be annotating the peak, as secondary alternative features (peak_10).       
	If there was a 3rd query given, the 3d feature would be parsed for annotation only if the 2nd query had failed to find a valid feature-hit, and so on. 

	The Best_hits in a query of priority=True, can report better the closest feature, when more than one are found (e.g peak_10), either for the Query-0 or for the secondary queries.   
	
	| peak_id | p_chr | p_start  | p_center | p_end    | feature    | f_start  | f_end    | f_strand | distance | gene_name  | Query | 
	|:--------|:------|:---------|:---------|:---------|:-----------|:---------|:---------|:---------|:---------|:-----------|:------| 
	| peak_1  | chr21 | 26932550 | 26945255 | 26957959 | NA         | NA       | NA       | NA       | NA       | NA         | 0,1   | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_6  | chr7  | 5562617  | 5567820  | 5573023  | gene       | 5567734  | 5567817  | -        | 3        | AC006483.1 | 0     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 
	| peak_10 | chr1  | 28832002 | 28836390 | 28840778 | transcript | 28836589 | 28862538 | +        | 199      | RCC1       | 1     | 
	| ...     |       |          |          |          |            |          |          |          |          |            |       | 

So, in the case of 'priority' =True, the features are mutually exclusive, and the rest of the queries should be parsed for valid hits in an escalating-priority, too.        
In case no feature-hit was found from any query, all the queries’ IDs will be reported with the non-annotated peak (NA).  
Example for the feature position 
-------------------------------- 
UROPA allows flexibility and at the same time robustness of annotation for features that are overlapping with their center, start or end position on a peak,      
but cannot always be annotated if only distance from TSS position is measured, as is the case in most annotation tools. The 'feature.position' key        
allows the values ['start', 'center', 'end'], so if a feature’s center or end position is closer to a peak, it will not be missed from the annotation.   
When one is not sure about which position is best to use, the default values allow running a position-free annotation,              
because all positions will be measured by default and the one with minimum distance from the peak center will allow for the closest feature to annotate the corresponding peak.         
An example follows, showing two annotations with different 'feature.position', the queries looked as followed:  
"queries":  [{"feature":"gene", "attribute":"gene_name", "distance":[5000],"feature.position": "start"}, 
		  {"feature": "gene", "feature.position": "center"}],
"internal"="False"
The annotation from UROPA given in All_hits and Best_hits tables, according to the queries, is shown below:

| peak_id | p_chr | p_start  | p_center | p_end    | feature | f_start  | f_end    | f_strand | distance | gene_name | Query | 
|:--------|:------|:---------|:---------|:---------|:--------|:---------|:---------|:---------|:---------|:----------|:------|
| ...     |       |          |          |          |         |          |          |          |          |           |       | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | NA      | NA       | NA       | NA       | NA       | NA        | 0     | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | gene    | 18111621 | 18213388 | +        | 1063     | BCL2L13   | 1     | 
| ...     |       |          |          |          |         |          |          |          |          |           |       | 

![peak71](img/chr22-18161287-18161496_peak71_h3k4me1_feature_pos.png)

As it is illustrated in the image, the peak is found in the gene body of BCL2L13, this is why the Query-0 doesn’t give any annotation in the above results.      
On the contrary, it is proven that the 'feature.position' = 'center' is closer than the start position (Distance = 1063) and can allow for annotation with the gene.
For the start it is actually:
feature.start – peak.center = \|18111621-18161442\| = 49 821  
But this distance is larger than 5000, which is the threshold given from the queries, this is why the gene is not annotated for the query 0.     
Therefore, this example shows that 'feature.position' is an important parameter that can assure a more precise annotation in similar cases,     
where a histone mark is acting in the gene body and not in the TSS, as for example the mark H3K4me1 used for the example.

Example for the direction 
------------------------- 
This example is based on H3K4me1 peaks annotated with the Gencode genome.
In the following example the utility of the key 'direction' will be illustrated. It is optional but can be very important 'player' for a more specialized annotation.             
It can also be thought of as the location of the peak depending on the feature’s direction. 

When direction is 'upstream', features accepted will be the ones that are closer with their start position (TSS) to the peak center.           
So, in this case we can say that the peak is upstream of the feature. On the other side, when direction is chosen 'downstream',              
the features annotated will be the ones that are closer with their ending position (TES) to the peak center. So, the peak would then be downstream of the feature.           
This is why the direction is relative to the peak location. An overlap is partially allowed to the edges of the peak, but the overlap should allow a clear evidence         
of the upstream or downstream location of the peak from the feature, so there shouldn’t be an important overlap of the peak length.

Let’s see now an example of an annotation with and without direction chosen, for the peak shown in Image 3.
![direction.key](img/chr1-1,403,500-1,408,500-01_h3k4me1_peaks.png)    
If the query looks as followed:         
"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000}]        
The peak displayed in the Figure would be annotated for both genes: 
ATAD3C with a distance of 712.5 bp and ATAD3B with a distance of 892.5 bp. Due to that no feature.position was defined, the distance calculated for ATAD3C        
is the distance from the gene end and the distance for ATAD3B the distance to the gene start. The best annotation in this case would than be the gene ATAD3C.    
More specific annotation can be usefull for some peaks. For example, if the peaks are known to be enriched in transcriptionally active promotors.   
It is possible to add the direction key with 'upstream' to the querie:          
"queries": [{"feature": "gene", "attribute":"gene_name", "distance":1000, "direction":"upstream"}]           
In this case the peak will only be annotated for ATAD3B. Depending on the biologically relevance, it is very usefull to utilize the accessible keys. 





Example for the internal.feature key
------------------------------------
This example is based on POLR2A peaks annotated with the Ensembl genome.         
When peaks are very large sometimes, the genomic features found inside the peak region are found to be far from the peak center and are thus discarded      
from the annotation. But, with the option of 'internal.features' UROPA allows to annotate the large peaks as well, with small features that can be of         
particular interest. Especially, when ATACseq peaks are used for annotating them with very small transcription factors, this option can become very handy.          
The following configuration allows for searching peaks internal features and featurs internal of peaks:
"queries":[{"feature":"gene", "distance":1000, "attribute":"gene_name"}],
"internal.features": "True"
The output would be:   
 
| p_chr   | p_start  | p_center | p_end | feature  | f_start  | f_end | f_strand | distance | gene_name| Query   | 
|:--------|:---------|:---------|:---------|:------|:---------|:---------|:------|:---------|:----------|:-------| 
| ...     |          |          |          |       |          |          |       |          |           |        | 
| chr6    | 27857165 | 27860401 | 27863637 | gene  | 27861203 | 27861669 | +     | 0        | HIST1H2BO | 0      | 
| chr6    | 27857165 | 27860401 | 27863637 | gene  | 27858093 | 27860884 | -     | 0        | HIST1H3J  | 0      | 
| chr6    | 27857165 | 27860401 | 27863637 | gene  | 27860477 | 27860963 | -     | 0        | HIST1H2AM | 0      | 
| ...     |          |          |          |       |          |          |       |          |           |        | 

![internal.feature](img/chr6-27,857,165-27,863,637_internal_feature-01.png)

We observe that UROPA annotated three genes in the region of the peak, as seen also in the Image 4.     
Their Distance is reported ‘Zero(0)’, because UROPA detects the internal features by their position even when their distances from the peak.center           
are further than the allowed 'distance' in the config, so the distance is not a parameter that can allow the annotation, this is why Zero value(0)           
is selected for ease of annotation in this special case.   
In the contrary case, where the option 'internal.feature' is not activated and no feature.position is chosen,          
the peak would only be annotated for HIST1H3J with a distance of 483 bp. 

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