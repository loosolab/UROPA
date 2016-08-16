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

| peak_id | p_chr | p_start  | p_center   | p_end    | feature | f_start  | f_end   | f_strand| distance | gene_name   | Query | 
|:--------|:------|:---------|:-----------|:---------|:--------|:---------|:--------|:--------|:---------|:------------|:------| 
| ...     |       |          |            |          |         |          |         |         |          |             |       | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17493294 | 17493822| +       | 23242.0  | AC006548.26 | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17442826 | 17489112| -       | 27952.0  | GAB4        | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17548711 | 17551565| +       | 31647.0  | AC006946.16 | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17517460 | 17541715| +       | 396.0    | CECR7       | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17561591 | 17562346| +       | 44527.0  | AC006946.17 | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17574502 | 17574829| -       | 57438.0  | AC006946.12 | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17565844 | 17596583| +       | 48780.0  | IL17RA      | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17602476 | 17612994| +       | 85412.0  | AC006946.15 | 0     | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17597189 | 17602257| -       | 80125.0  | CECR6       | 0     | 
| ...     |       |          |            |          |         |          |         |         |          |             |       | 

Table 1: All hits table basic example
2. Besthit_table_basic_example.txt

| peak_id | p_chr | p_start  | p_center   | p_end    | feature | f_start | f_end   | f_strand | distance | gene_name | Query | 
|:--------|:------|:---------|:-----------|:---------|:--------|:--------|:--------|:---------|:---------|:----------|:------| 
| ...     |       |          |            |          |         |         |         |          |          |           |       | 
| peak13  | chr22 | 17516785 | 17517064.0 | 17517343 | gene    | 17517460| 17541715| +        | 396.0    | CECR7     | 0     | 
| ...     |       |          |            |          |         |         |         |          |          |           |       | 

Table 2: Best hits table basic example
3. Reformatted_Allhits_perPeak_basic_anno.txt

| peak_id | p_chr | p_start  | p_center | p_end    | Query | Merged_Info                                                                                                  | 
|:--------|:------|:---------|:---------|:---------|:------|:-------------------------------------------------------------------------------------------------------------| 
| ...     |       |          |          |          |       |                                                                                                              | 
| peak13  | chr22 | 17516785 | 17517064 | 17517343 | 0     | feature:gene; f_start:17493294,17442826,17548711,17517460,17561591,17574502,17565844,17602476,17597189;   | 
|         |       |          |          |          |       | f_end:17493822,17489112,17551565,17541715,17562346,17574829,17596583,17612994,17602257;                   | 
|         |       |          |          |          |       | f_strand:+,-,+,+,+,-,+,+,-; distance:23242,27952,31647,396,44527,57438,48780,85412,80125;  | 
|         |       |          |          |          |       | gene_name:AC006548.26,GAB4,AC006946.16,CECR7,AC006946.17,AC006946.12,IL17RA,AC006946.15,CECR6                | 
| ...     |       |          |          |          |       |                                                                                                              | 

Table 3: Reformatted Allhits perPeak basic anno. Notice that the last colum is just adjusted to more rows for display them.  

**TODO** What about Merged Best hits table??
**TODO** Summary to come