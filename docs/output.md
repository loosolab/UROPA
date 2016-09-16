UROPA provides many output files,each providing a valuable information in a more extended either more condense way, to cover all needs.

The different outputs are shown with the following example:

H3K4me1 peaks from UCSC (processed data accession 'ENCFF001SUE') were annotated for genes from gencode.v19 gtf file. ([further details](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files)) using almost default values: 
`  
{"queries": [{"feature":"gene", "show.attributes":"gene_id"}],  
"GTF": "gencode.v19.annotation.GTF",  
"bed": "ENCFF001SUE.bed"} `

**Important Note** 
Make sure to give any attributes for display in the output-if existant in the 9th column of the gtf - otherwise the annotated peaks will be reported 
without any information of the assigned features.

To make it easier, the feature was set on 'gene' in this example. 

Running UROPA with:     
```
uropa.sh -i config.json -o basic_example -r
```    

There will be three output tables in the folder 'basic_example/'. 
The flag '-r' will create the reformatted table of the Best_hits where each peak contains all annotation of all queries in one line. 
(peak names are given manually)

1. Allhits_table_basic_example.txt

| peak_id | p_chr | p_start   | p_center    | p_end     | feature | feat_start   | feat_end     | feat_strand | distance | gene_id      | query | 
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

*[Table 1: All hits table basic example]*

2. Besthit_table_basic_example.txt

| peak_id | p_chr | p_start   | p_center    | p_end     | feature | feat_start   | feat_end     | feat_strand | distance | gene_id   | query | 
|---------|-------|-----------|-------------|-----------|---------|-----------|-----------|----------|----------|-----------|-------| 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NR_046000 | 0     | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | CDS     | 405018    | 405130    | +        | 189.0    | NM_002460 | 1     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 0     | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 1     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324293 | 106324344 | -        | 181.0    | NR_039730 | 0     | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | NA      | NA        | NA        | NA       | NA       | NA        | 1     | 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 

[Table 2: Best hits table basic example]

3. Merged_best_hits_basic_example

| peak_id | p_chr | p_start   | p_center    | p_end     | feature | feat_start   | feat_end     | feat_strand | distance | gene_id   | query | 
|---------|-------|-----------|-------------|-----------|---------|-----------|-----------|----------|----------|-----------|-------| 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 
| peak_3  | chr6  | 396914    | 405319.0    | 413724    | exon    | 405018    | 405130    | +        | 189.0    | NR_046000 | 0,1   | 
| peak_4  | chr17 | 56404303  | 56411344.0  | 56418385  | NA      | NA        | NA        | NA       | NA       | NA        | 0,1   | 
| peak_5  | chr14 | 106317273 | 106324112.0 | 106330951 | exon    | 106324293 | 106324344 | -        | 181.0    | NR_039730 | 0     | 
| ...     |       |           |             |           |         |           |           |          |          |           |       | 

Table 3: Merged best hits basic example

4. Reformatted_Allhits_perPeak_basic_anno.txt

| peak_id | p_chr | p_start   | p_center  | p_end     | feature   | feat_start       | feat_end         | feat_strand | distance | gene_id              | query | 
|---------|-------|-----------|-----------|-----------|-----------|---------------|---------------|----------|----------|----------------------|-------| 
| ...     |       |           |           |           |           |               |               |          |          |                      |       | 
| peak_3  | chr6  | 396914    | 405319    | 413724    | exon, CDS | 405018        | 405130        | +        | 189      | NR_046000, NM_002460 | 0,1   | 
| peak_4  | chr17 | 56404303  | 56411344  | 56418385  | NA        | NA            | NA            | NA       | NA       | NA                   | 0,1   | 
| peak_5  | chr14 | 106317273 | 106324112 | 106330951 | exon, NA  | 106324293, NA | 106324344, NA | -,NA     | 181,NA   | NR_039730, NA        | 0,1   | 
| ...     |       |           |           |           |           |               |               |          |          |                      |       | 

[Table 4: Reformatted Allhits per Peak basic anno. Notice that the last column is just adjusted to more rows for display them.]

#Output columns explanation
**feature, feature_start, feature_end, feature_strand** : The information of the genomic feature that annotates the peak, as extracted by the gtf file.

**distance** : The distance measured as following: abs(peak.center-feature.position).If no feature.position given,then the minimum of 3 distances from each feature.position{start,center,end} to peak.center is chosen.

**feat_pos**: The position of the genomic feature chosen for annotation that had the minimum distance to the peak.center.If feature.position given in config this will be shown also here.

**genomic_location**: The position of the peak relative to the annotated feature direction.(i.e upstream = peak located upstream of the gene).

**feat_ovl_peak**: When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / peak.length) shows percentage of peak covered by the feature.(i.e 1.0 = 100% of peak covered, peak is internal.

**peak_ovl_feat**: When peak and feature overlap(i.e genomic_location = overlapStart), Ratio(overlapping region / feature.length) shows percentage of feature covered by the peak.(i.e 1.0 = 100% of feature covered, feature is internal.)

**gene_name, gene_id, gene_type** : Attributes that have been given in the key 'show.atttributes' will be shown here and their values extracted by the gtf will be displayed for each feature.If 'filter.attribute' contains same attribute keys, this column helps confirming the filtering.

**query**: The query that validates with its given parameters the feature to be assigned to the peak.If only one query given, column will always display '0',the first query.


6. Summary of UROPA output
For every run there is also a summary output, vizualising the results for a global overview of the final annotation. Within this document one can find : 
-> Graphs based on the 'Best Hits' output:
* A pairwise comparison among all queries is evaluated within a venn diagram, when more than one query is given in the config file. 
* A distribution of the distances per feature per query are displayed in a histogram.
* A pie chart illustrating the genomic location of the peaks per annotated feature.
* A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation.

-> Graphs based on the 'Merged Best Hits' output:
* A density plot displaying the distance per feature per query. 
* A pie chart illustrating the genomic locations of the peaks per annotated feature.
* A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation.
