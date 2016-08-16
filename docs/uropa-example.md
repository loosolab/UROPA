Configuration file Usage
=========================
In this section several examples for the usage of the configuration files are presented. 

Example with two queries and difference in priority 
--------------------------------------------------- 
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
	|---------|-------|----------|----------|----------|------------|----------|----------|----------|----------|------------|-------| 
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
	|---------|-------|----------|----------|----------|------------|----------|----------|----------|----------|------------|-------| 
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
|---------|-------|----------|----------|----------|---------|----------|----------|----------|----------|-----------|-------| 
| ...     |       |          |          |          |         |          |          |          |          |           |       | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | NA      | NA       | NA       | NA       | NA       | NA        | 0     | 
| peak71  | chr22 | 18161387 | 18161442 | 18161496 | gene    | 18111621 | 18213388 | +        | 1063     | BCL2L13   | 1     | 
| ...     |       |          |          |          |         |          |          |          |          |           |       | 

![peak71](img/chr22-18161287-18161496_peak71_h3k4me1_feature_pos.png

As it is illustrated in the image, the peak is found in the gene body of BCL2L13, this is why the Query-0 doesn’t give any annotation in the above results.      
On the contrary, it is proven that the “feature.position” = “center” is closer than the start position (Distance = 1063) and can allow for annotation with the gene.
For the start it is actually:
feature.start – peak.center = \|18111621-18161442\| = 49 821  
But this distance is larger than 5000, which is the threshold given from the queries, this is why the gene is not annotated for the query 0.     
Therefore, this example shows that 'feature.position' is an important parameter that can assure a more precise annotation in similar cases,     
where a histone mark is acting in the gene body and not in the TSS, as for example the mark H3K4me1 used for the example.

Example for the direction 
------------------------- 

Example for the internal.feature key
------------------------------------
When peaks are very large sometimes, the genomic features found inside the peak region are found to be far from the peak center and are thus discarded      
from the annotation. But, with the option of “internal.features” UROPA allows to annotate the large peaks as well, with small features that can be of         
particular interest. Especially, when ATACseq peaks are used for annotating them with very small transcription factors, this option can become very handy.

Used peak and annotation files 
------------------------------ 
Annotation:  
Ensembl database of the human genome, version hg19 (GRC37): [Ensembl genome](ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/) 
Human Gencode genome, version hg19: [Gencode genome](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_19/) 

Narrow peak and signal files based on ChIP-seq of GM12878 immortalized cell line:  
[H3K4ME1](https://www.encodeproject.org/experiments/ENCSR000AKF/)   
[POLR2A](https://www.encodeproject.org/experiments/ENCSR000EAD/)     
**Note**: peak ids are manually added to make it easier to compare different tables or to combind tables with images. 

Still not sure how to use the config file? Please contact [Maria Kondili](maria.kondili@mpi-bn.mpg.de)