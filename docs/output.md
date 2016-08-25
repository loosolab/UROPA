UROPA provides many output files. The different outputs are showns with an example:

H3K4me1 peaks from UCSC (processed data accession ENCFF001SUE were annotated for genes from gencode v19 ([further details](#"Used peak and annotation files")) using almost default values:   
{"queries":[{"feature":"gene", "attribute":"gene_name"}],  
"gtf": "gencode.v19.annotation.gtf",  
"bed": "ENCFF001SUE.bed"}  
To make it easier, the feature was set on gene. Otherwise it is possible that thare are thousands of valid annotations for one peak.        
But whatever should be analysed, it is possible to leave out this key as well. 
Of course, the attribute key cannot be left out, this is what the peaks will be annotated for.     
Running UROPA with:     
```
uropa.sh -i config.json -o basic_example -r
```    
There will be three output tables in the folder basic_example: 
(peak names are given manually)

1. Allhits_table_basic_example.txt

| peak_id | p_chr | p_start   | p_center    | p_end     | feature | f_start   | f_end     | f_strand | distance | gene_id      | query | 
|---------|-------|-----------|-------------|-----------|---------|-----------|-----------|----------|----------|--------------|-------| 
| ...     |       |           |             |           |         |           |           |          |          |              |       | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NR_046000    | 0     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NM_001195286 | 0     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NM_002460    | 0     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 401424    | 401777    | +        | 3542.0   | NM_001195286 | 1     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 405018    | 405130    | +        | 189.0    | NM_002460    | 1     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 405018    | 405130    | +        | 189.0    | NM_001195286 | 1     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 401424    | 401777    | +        | 3542.0   | NM_002460    | 1     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 407455    | 407595    | +        | 2136.0   | NM_002460    | 1     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 407455    | 407595    | +        | 2136.0   | NM_001195286 | 1     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA           | 0     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA           | 1     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324293 | 106324344 | -        | 181.0    | NR_039730    | 0     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324334 | 106324411 | -        | 222.0    | NR_130467    | 0     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | NA      | NA        | NA        | NA       | NA       | NA           | 1     | 
| ...     |       |           |             |           |         |           |           |          |          |              |       | 



Table 1: All hits table basic example
2. Besthit_table_basic_example.txt

| peak_id | p_chr | p_start   | p_center    | p_end     | feature | f_start   | f_end     | f_strand | distance | gene_id   | query | 
|---------|-------|-----------|-------------|-----------|---------|-----------|-----------|----------|----------|-----------|-------| 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NR_046000 | 0     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 405018    | 405130    | +        | 189.0    | NM_002460 | 1     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 0     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 1     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324293 | 106324344 | -        | 181.0    | NR_039730 | 0     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | NA      | NA        | NA        | NA       | NA       | NA        | 1     | 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 


Table 2: Best hits table basic example

3. Merged_best_hits_basic_example
| peak_id | p_chr | p_start   | p_center    | p_end     | feature | f_start   | f_end     | f_strand | distance | gene_id   | query | 
|---------|-------|-----------|-------------|-----------|---------|-----------|-----------|----------|----------|-----------|-------| 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NR_046000 | 0,1   | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 0,1   | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324293 | 106324344 | -        | 181.0    | NR_039730 | 0     | 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 

Table 3: Merged best hits basic example
4. Reformatted_Allhits_perPeak_basic_anno.txt

| peak_id | p_chr | p_start   | p_center  | p_end     | feature  | f_start      | f_end        | f_strand | distance | gene_id             | query | 
|---------|-------|-----------|-----------|-----------|----------|--------------|--------------|----------|----------|---------------------|-------| 
| ...     |       |           |           |           |          |              |              |          |          |                     |       | 
| peak_3  | chr6  | 396914    | 405319    | 413724    | exon,CDS | 405018       | 405130       | +        | 189      | NR_046000,NM_002460 | 0,1   | 
| peak_4  | chr17 | 56404303  | 56411344  | 56418385  | NA       | NA           | NA           | NA       | NA       | NA                  | 0,1   | 
| peak_5  | chr14 | 106317273 | 106324112 | 106330951 | exon,NA  | 106324293,NA | 106324344,NA | -,NA     | 181,NA   | NR_039730,NA        | 0,1   | 
| ...     |       |           |           |           |          |              |              |          |          |                     |       | 


Table 4: Reformatted Allhits perPeak basic anno. Notice that the last colum is just adjusted to more rows for display them.  

5. Summary of UROPA run
For every run there is also a summary output. Within this there are various plot to communicate an overview about the run. There are different plots:
* if there is more than one query, a pairwise comparison of all queries is evaluated within a venn diagramm based on the best hits output
* the distance per feature per query are displayed in a histogram based on the best hits output
* the genomic location per feature in a pie chart based on the best hits output 
* if there is more than one feature, the occurence of the different features are displayed in a barplot based on the best hits output
* the distance per feature per query are displayed in a density plot based on the merged best hits output 
* the genomic location per feature in a pie chart based on the merged best hits output
* if there is more than one feature, the occurence of the different features are displayed in a barplot based on the merged best hits output
