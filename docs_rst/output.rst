Output tables
=============
UROPA provides many output files, each providing valuable information in either a more extended or a more condense way, to cover all needs and be useful for further analyses.

The different outputs will be explained thoroughly below.

File overview
-------------
- **Uropa_AllHits**  : The basic output table giving for each peak all valid annotations and additionally NA rows for invalid annotations.

- **Uropa_FinalHits** : The table which can be the most useful for peak annotation.It provides the best-selected feature according to the config criteria for annotating each peak. The closest distance is the basic parameter for the selection. It also summarizes the 'BestperQuery_Hits' by chosing the closest feature for each peak in case more queries are given and each query validates a different feature.

- **Uropa_BestperQuery_Hits** : Only if more than one query is specified: Best valid annotation per query for each peak.

- **Uropa_Reformatted_HitsperPeak** : Only if more than one query is specified and the *-r* parameter is used: Compact table with best per query annotation in one row. 

- **Uropa_Summary** : Only if the *-s* parameter is used: Graphical information of the peak annotation run by UROPA.

.. note::
	The output files will be named additionally by the output directory name where they are located, for convenience in further use and transfer of files.
	Example  : ChIPannot/Uropa_AllHits_ChIPannot.txt

Output columns explanation
--------------------------

The four output tables mentioned above contain many informative columns about the peak annotation performed. The headers and content of tables are explained here:

- **peak_id, peak_start, peak_center, peak_end, peak_strand**: Peak information with id if available, otherwise a peak id in chr:start-end format will be created.

- **feature, feat_start, feat_end, feat_strand**: The information of the genomic feature that annotates the peak, as extracted by the gtf file.

- **feat_anchor**: The position of the genomic feature annotated, having the minimum distance to the peak_center. If 'feature.anchor' given in config only this will be used.

- **distance** : The distance measured as following: _abs(peak_center-feature_anchor)_. If no feature.anchor is given, the minimum of all feature.anchor {start,center,end} to peak_center is chosen.

- **genomic_location**: The position of the peak relative to the annotated feature direction (e.g. upstream = peak located upstream of the gene, see `Figure 2 <http://www.ensembl.org/info/website/upload/gff.html%3E>`_.

- **feat_ovl_peak**: Percentage of how much the peak is coverd by the feature (1.0 = 100%, this correspond to the genomic_location "PeakInsideFeature").

- **peak_ovl_feat**: Percentage of how much the feature is coverd by the peak (1.0 correspond to the genomic_location "FeatureInsidePeak").

- **gene_name, gene_id, gene_type,...** : Attributes that have been given in the key 'show.atttributes' will be shown here with their values extracted by the GTF.

.. hint:: 
	If 'filter.attribute' contains same attribute keys, this column helps confirming the filtering.

.. note:: 
	Make sure to give any attributes for display in the output-if existant in the 9th column of the gtf - otherwise the annotated peaks will be reported without any information of the assigned features.

- **query**: The query that validates with its given parameters the feature to be assigned to the peak.If only one query given, column will always display '0',the first query.


Output files (one query)
------------------------
UROPA annotation with one query results in two output tables. Those are the Uropa_AllHits and Uropa_FinalHits. 
With a configuration as followed, a cut out of the AllHits would look as in Table 1, and a cut out of the FinalHits as displayed in Table 2. Peak and annotation files are further described [here](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files). 
The UROPA annotation process for one query can run into three cases for each peak, those are:

* **Case 1**: No query gives any feature for annotating the peaks, this leads to no valid annotation at all -> NA row in AllHits and FinalHits. 
	
* **Case 2**: There is one valid annotation for the specified query -> annotation will be given in AllHits and FinalHits. 
	
* **Case 3**: There are multiple valid anntoations for the specified query -> all valid annotations will be given in the AllHits, the best annotation (smallest distance) will be presented in the FinalHits.  


.. code:: json

    {
    "queries":[
            {"feature":"gene", "distance":10000, "feature.anchor":"start", "internals":"True", 
                "filter.attribute":"gene_type", "attribute.value":"protein_coding",
                "show.attributes":["gene_name","gene_type"]}], 
     "priority" : "False",
     "gtf":"gencode.v19.annotation.gtf" ,
     "bed":"ENCFF001VFA.bed"
    }
	
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | pea | peak | peak | pea |   | fea | feat | fea | feat | dis | feat | genomi | feat\ | peak\ | gen | gene\ | qu |
| k\_ | k\_ | \_st | \_ce | k\_ |   | tur | \_st | t\_ | \_st | tan | \_an | c\_loc | _ovl\ | _ovl\ | e\_ | _type | er |
| id  | chr | art  | nter | end |   | e   | art  | end | rand | ce  | chor | ation  | _peak | _feat | nam |       | y  |
|     |     |      |      |     |   |     |      |     |      |     |      |        |       |       | e   |       |    |
+=====+=====+======+======+=====+===+=====+======+=====+======+=====+======+========+=======+=======+=====+=======+====+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 0  |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 355 |     |      |      | 98  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | gen | 4388 | 439 | -    | 253 | star | overla | 0.57  | 0.09  | HNR | prote | 0  |
| k\_ | 10  | 2516 | 4360 | 062 |   | e   | 1065 | 046 |      |     | t    | pStart |       |       | NPF | in\_c |    |
| 356 |     |      | .5   | 05  |   |     |      | 14  |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 9826 | 9826 | 982 | . | gen | 9819 | 982 | -    | 261 | star | upstre | 0.0   | 0.0   | CHD | prote | 0  |
| k\_ | 5   | 2863 | 4852 | 668 |   | e   | 0908 | 622 |      | 2   | t    | am     |       |       | 1   | in\_c |    |
| 765 |     |      | .5   | 42  |   |     |      | 40  |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 1758 | 1758 | 175 | . | gen | 1758 | 175 | -    | 937 | star | overla | 0.31  | 0.3   | NOP | prote | 0  |
| k\_ | 5   | 1450 | 1691 | 819 |   | e   | 1094 | 815 |      |     | t    | pStart |       |       | 16  | in\_c |    |
| 769 |     | 8    | 3.5  | 319 |   |     | 9    | 976 |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 1758 | 1758 | 175 | . | gen | 1758 | 175 | +    | 116 | star | Featur | 0.22  | 1.0   | HIG | prote | 0  |
| k\_ | 5   | 1450 | 1691 | 819 |   | e   | 1574 | 816 |      | 5   | t    | eInsid |       |       | D2A | in\_c |    |
| 769 |     | 8    | 3.5  | 319 |   |     | 8    | 772 |      |     |      | ePeak  |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 1758 | 1758 | 175 | . | gen | 1757 | 175 | +    | 244 | star | PeakIn | 1.0   | 0.14  | ARL | prote | 0  |
| k\_ | 5   | 1450 | 1691 | 819 |   | e   | 9247 | 828 |      | 42  | t    | sideFe |       |       | 10  | in\_c |    |
| 769 |     | 8    | 3.5  | 319 |   |     | 1    | 866 |      |     |      | ature  |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+



Table 1: AllHits for one query The column order is: peak_id, peak_chr, peak_start, peak_center, peak_end, peak_strand, feature, feat_start, feat_end, feat_strand, distance, feat_anchor, genomic_location, feat_ovl_peak, peak_ovl_feat, gene_name, gene_type, query

+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | pea | peak | peak | pea |   | fea | feat | fea | feat | dis | feat | genomi | feat\ | peak\ | gen | gene\ | qu |
| k\_ | k\_ | \_st | \_ce | k\_ |   | tur | \_st | t\_ | \_st | tan | \_an | c\_loc | _ovl\ | _ovl\ | e\_ | _type | er |
| id  | chr | art  | nter | end |   | e   | art  | end | rand | ce  | chor | ation  | _peak | _feat | nam |       | y  |
|     |     |      |      |     |   |     |      |     |      |     |      |        |       |       | e   |       |    |
+=====+=====+======+======+=====+===+=====+======+=====+======+=====+======+========+=======+=======+=====+=======+====+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 0  |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 355 |     |      | .0   | 98  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | gen | 4388 | 439 | -    | 253 | star | overla | 0.57  | 0.09  | HNR | prote | 0  |
| k\_ | 10  | 2516 | 4360 | 062 |   | e   | 1065 | 046 |      |     | t    | pStart |       |       | NPF | in\_c |    |
| 356 |     |      | .5   | 05  |   |     |      | 14  |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 9826 | 9826 | 982 | . | gen | 9819 | 982 | -    | 261 | star | upstre | 0.0   | 0.0   | CHD | prote | 0  |
| k\_ | 5   | 2863 | 4852 | 668 |   | e   | 0908 | 622 |      | 2   | t    | am     |       |       | 1   | in\_c |    |
| 765 |     |      | .5   | 42  |   |     |      | 40  |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 1758 | 1758 | 175 | . | gen | 1758 | 175 | -    | 937 | star | overla | 0.31  | 0.3   | NOP | prote | 0  |
| k\_ | 5   | 1450 | 1691 | 819 |   | e   | 1094 | 815 |      |     | t    | pStart |       |       | 16  | in\_c |    |
| 769 |     | 8    | 3.5  | 319 |   |     | 9    | 976 |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+


Table 2: FinalHits for one query. The column order is: peak_id, peak_chr, peak_start, peak_center, peak_end, peak_strand, feature, feat_start, feat_end, feat_strand, distance, feat_anchor, genomic_location, feat_ovl_peak, peak_ovl_feat, gene_name, gene_type, query

As displayed in Table 1 and 2, peak_355 is a representative of Case 1. There is no valid annotation at all, there is an NA row in both output tables. 
The peaks 356 and 765 belong to Case 2, there is one valid annotation for them, their annotation is displayed in the same way in AllHits and FinalHits (Table 1 and 2). 
Whereas peak_769 has three valid annotations for the specified query. All of them are displayed in the AllHits output (Table 1). In the FinalHits only the best annotation, the one for gene NOP16 with the minimal distance of 937 is represented in the FinalHits (Table 2).


Output files (multiple queries)
--------------------------------
UROPA annotation with multiple queries result in at least three output tables. Those are the Uropa_AllHits, Uropa_FinalHits, and Uropa_BestperQuery_Hits. If the *-r* parameter is added in the command line call, there will the additional output Uropa_Reformatted_HitsperPeak file.
With a configuration as followed, a cut out of all generated output files will look as in Table 3 to 6 and Figure 1. Peak and annotation files are further discribed [here](http://uropa.readthedocs.io/en/latest/uropa-example/#used-peak-and-annotation-files). 
The UROPA annotation process for multiple queries can run into one more case as described for one query:

- **Case 1 to 3** as described above

- **Case 4**: There are valid annotations for multiple queries -> all valid annotations will be given in the AllHits, the best annotation (smallest distance across all queries) will be presented in the FinalHits. 

.. code:: json

    {
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

+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | pea | pea | peak | pea | peak | fea | fea | fea | feat | dis | feat | genom | feat | peak | gen | gene\ | qu |
| k\_ | k\_ | k\_ | \_ce | k\_ | \_st | tur | t\_ | t\_ | \_st | tan | \_an | ic\_l | \_ov | \_ov | e\_ | _type | er |
| id  | chr | sta | nter | end | rand | e   | sta | end | rand | ce  | chor | ocati | l\_p | l\_f | nam |       | y  |
|     |     | rt  |      |     |      |     | rt  |     |      |     |      | on    | eak  | eat  | e   |       |    |
+=====+=====+=====+======+=====+======+=====+=====+=====+======+=====+======+=======+======+======+=====+=======+====+
| …   |     |     |      |     | .    |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 792 | 7921 | 792 | .    | NA  | NA  | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA  | NA    | 0  |
| k\_ | 15  | 115 | 7124 | 226 |      |     |     |     |      |     |      |       |      |      |     |       |    |
| 355 |     | 50  | .0   | 98  |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 792 | 7921 | 792 | .    | NA  | NA  | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA  | NA    | 1  |
| k\_ | 15  | 115 | 7124 | 226 |      |     |     |     |      |     |      |       |      |      |     |       |    |
| 355 |     | 50  | .0   | 98  |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 792 | 7921 | 792 | .    | NA  | NA  | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA  | NA    | 2  |
| k\_ | 15  | 115 | 7124 | 226 |      |     |     |     |      |     |      |       |      |      |     |       |    |
| 355 |     | 50  | .0   | 98  |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 439 | 4390 | 439 | .    | gen | 438 | 439 | -    | 253 | star | overl | 0.57 | 0.09 | HNR | prote | 0  |
| k\_ | 10  | 025 | 4360 | 062 |      | e   | 810 | 046 |      |     | t    | apSta |      |      | NPF | in\_c |    |
| 356 |     | 16  | .5   | 05  |      |     | 65  | 14  |      |     |      | rt    |      |      |     | oding |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 439 | 4390 | 439 | .    | NA  | NA  | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA  | NA    | 1  |
| k\_ | 10  | 025 | 4360 | 062 |      |     |     |     |      |     |      |       |      |      |     |       |    |
| 356 |     | 16  | .5   | 05  |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 439 | 4390 | 439 | .    | NA  | NA  | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA  | NA    | 2  |
| k\_ | 10  | 025 | 4360 | 062 |      |     |     |     |      |     |      |       |      |      |     |       |    |
| 356 |     | 16  | .5   | 05  |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| …   |     |     |      |     |      |     |     |     |      |     |      |       |      |      |     |       |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| pea | chr | 982 | 9826 | 982 | .    | gen | 981 | 982 | -    | 261 | star | upstr | 0.0  | 0.0  | CHD | prote | 0  |
| k\_ | 5   | 628 | 4852 | 668 |      | e   | 909 | 622 |      | 2   | t    | eam   |      |      | 1   | in\_c |    |
| 765 |     | 63  | .5   | 42  |      |     | 08  | 40  |      |     |      |       |      |      |     | oding |    |
+-----+-----+-----+------+-----+------+-----+-----+-----+------+-----+------+-------+------+------+-----+-------+----+
| peak | ch | 9826 | 98264 | 9826 | . | ge | 9826 | 9833 | + | 22  | sta | overlap | 0. | 0. | CTD-20 | lincRN | 1 |
| \_76 | r5 | 2863 | 852.5 | 6842 |   | ne | 4875 | 0717 |   |     | rt  | Start   | 5  | 03 | 07H13. | A      |   |
| 5    |    |      |       |      |   |    |      |      |   |     |     |         |    |    | 3      |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 9826 | 98264 | 9826 | . | ge | 9827 | 9827 | - | 759 | sta | downstr | 0. | 0. | Y\_RNA | misc\_ | 2 |
| \_76 | r5 | 2863 | 852.5 | 6842 |   | ne | 2342 | 2451 |   | 8   | rt  | eam     | 0  | 0  |        | RNA    |   |
| 5    |    |      |       |      |   |    |      |      |   |     |     |         |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| …    |    |      |       |      |   |    |      |      |   |     |     |         |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | ge | 1758 | 1758 | - | 937 | sta | overlap | 0. | 0. | NOP16  | protei | 0 |
| \_76 | r5 | 1450 | 6913. | 1931 |   | ne | 1094 | 1597 |   |     | rt  | Start   | 31 | 3  |        | n\_cod |   |
| 9    |    | 8    | 5     | 9    |   |    | 9    | 6    |   |     |     |         |    |    |        | ing    |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | ge | 1758 | 1758 | + | 116 | sta | Feature | 0. | 1. | HIGD2A | protei | 0 |
| \_76 | r5 | 1450 | 6913. | 1931 |   | ne | 1574 | 1677 |   | 5   | rt  | InsideP | 22 | 0  |        | n\_cod |   |
| 9    |    | 8    | 5     | 9    |   |    | 8    | 2    |   |     |     | eak     |    |    |        | ing    |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | ge | 1757 | 1758 | + | 244 | sta | PeakIns | 1. | 0. | ARL10  | protei | 0 |
| \_76 | r5 | 1450 | 6913. | 1931 |   | ne | 9247 | 2886 |   | 42  | rt  | ideFeat | 0  | 14 |        | n\_cod |   |
| 9    |    | 8    | 5     | 9    |   |    | 1    | 6    |   |     |     | ure     |    |    |        | ing    |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | NA | NA   | NA   | N | NA  | NA  | NA      | NA | NA | NA     | NA     | 1 |
| \_76 | r5 | 1450 | 6913. | 1931 |   |    |      |      | A |     |     |         |    |    |        |        |   |
| 9    |    | 8    | 5     | 9    |   |    |      |      |   |     |     |         |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | NA | NA   | NA   | N | NA  | NA  | NA      | NA | NA | NA     | NA     | 2 |
| \_76 | r5 | 1450 | 6913. | 1931 |   |    |      |      | A |     |     |         |    |    |        |        |   |
| 9    |    | 8    | 5     | 9    |   |    |      |      |   |     |     |         |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+
| …    |    |      |       |      |   |    |      |      |   |     |     |         |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+---+-----+-----+---------+----+----+--------+--------+---+




   Table 3: AllHits for multiple queries. The column order is: peak_id, peak_chr, peak_start, peak_center, peak_end, peak_strand, feature, feat_start, feat_end, feat_strand, distance, feat_anchor, genomic_location, feat_ovl_peak, peak_ovl_feat, gene_name, gene_type, query

+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| pea | pea | peak | peak | pea |   | fea | feat | fea | feat | dis | feat | genom | feat | peak | gene | gene\ | qu |
| k\_ | k\_ | \_st | \_ce | k\_ |   | tur | \_st | t\_ | \_st | tan | \_an | ic\_l | \_ov | \_ov | \_na | _type | er |
| id  | chr | art  | nter | end |   | e   | art  | end | rand | ce  | chor | ocati | l\_p | l\_f | me   |       | y  |
|     |     |      |      |     |   |     |      |     |      |     |      | on    | eak  | eat  |      |       |    |
+=====+=====+======+======+=====+===+=====+======+=====+======+=====+======+=======+======+======+======+=======+====+
| …   |     |      |      |     |   |     |      |     |      |     |      |       |      |      |      |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA    | NA   | NA   | NA   | NA    | 0, |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |       |      |      |      |       | 1, |
| 355 |     |      | .0   | 98  |   |     |      |     |      |     |      |       |      |      |      |       | 2  |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | gen | 4388 | 439 | -    | 253 | star | overl | 0.57 | 0.09 | HNRN | prote | 0  |
| k\_ | 10  | 2516 | 4360 | 062 |   | e   | 1065 | 046 |      |     | t    | apSta |      |      | PF   | in\_c |    |
| 356 |     |      | .5   | 05  |   |     |      | 14  |      |     |      | rt    |      |      |      | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
|     |     |      |      |     |   |     |      |     |      |     |      |       |      |      |      |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| pea | chr | 9826 | 9826 | 982 | . | gen | 9826 | 983 | +    | 22  | star | overl | 0.5  | 0.03 | CTD- | lincR | 1  |
| k\_ | 5   | 2863 | 4852 | 668 |   | e   | 4875 | 307 |      |     | t    | apSta |      |      | 2007 | NA    |    |
| 765 |     |      | .5   | 42  |   |     |      | 17  |      |     |      | rt    |      |      | H13. |       |    |
|     |     |      |      |     |   |     |      |     |      |     |      |       |      |      | 3    |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
|     |     |      |      |     |   |     |      |     |      |     |      |       |      |      |      |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| pea | chr | 1758 | 1758 | 175 | . | gen | 1758 | 175 | -    | 937 | star | overl | 0.31 | 0.3  | NOP1 | prote | 0  |
| k\_ | 5   | 1450 | 1691 | 819 |   | e   | 1094 | 815 |      |     | t    | apSta |      |      | 6    | in\_c |    |
| 769 |     | 8    | 3.5  | 319 |   |     | 9    | 976 |      |     |      | rt    |      |      |      | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+
| …   |     |      |      |     |   |     |      |     |      |     |      |       |      |      |      |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+-------+------+------+------+-------+----+

Table 4: FinalHits for mulitple queries. The column order is: peak_id, peak_chr, peak_start, peak_center, peak_end, peak_strand, feature, feat_start, feat_end, feat_strand, distance, feat_anchor, genomic_location, feat_ovl_peak, peak_ovl_feat, gene_name, gene_type, query

+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | pea | peak | peak | pea |   | fea | feat | fea | feat | dis | feat | genomi | feat\ | peak\ | gen | gene\ | qu |
| k\_ | k\_ | \_st | \_ce | k\_ |   | tur | \_st | t\_ | \_st | tan | \_an | c\_loc | _ovl\ | _ovl\ | e\_ | _type | er |
| id  | chr | art  | nter | end |   | e   | art  | end | rand | ce  | chor | ation  | _peak | _feat | nam |       | y  |
|     |     |      |      |     |   |     |      |     |      |     |      |        |       |       | e   |       |    |
+=====+=====+======+======+=====+===+=====+======+=====+======+=====+======+========+=======+=======+=====+=======+====+
| …   |     |      |      |     |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 0  |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 355 |     |      | .0   | 98  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 1  |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 355 |     |      | .0   | 98  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 7921 | 7921 | 792 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 2  |
| k\_ | 15  | 1550 | 7124 | 226 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 355 |     |      | .0   | 98  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | gen | 4388 | 439 | -    | 253 | star | overla | 0.57  | 0.09  | HNR | prote | 0  |
| k\_ | 10  | 2516 | 4360 | 062 |   | e   | 1065 | 046 |      |     | t    | pStart |       |       | NPF | in\_c |    |
| 356 |     |      | .5   | 05  |   |     |      | 14  |      |     |      |        |       |       |     | oding |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 1  |
| k\_ | 10  | 2516 | 4360 | 062 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 356 |     |      | .5   | 05  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| pea | chr | 4390 | 4390 | 439 | . | NA  | NA   | NA  | NA   | NA  | NA   | NA     | NA    | NA    | NA  | NA    | 2  |
| k\_ | 10  | 2516 | 4360 | 062 |   |     |      |     |      |     |      |        |       |       |     |       |    |
| 356 |     |      | .5   | 05  |   |     |      |     |      |     |      |        |       |       |     |       |    |
+-----+-----+------+------+-----+---+-----+------+-----+------+-----+------+--------+-------+-------+-----+-------+----+
| …    |    |      |       |      |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 9826 | 98264 | 9826 | . | ge | 9819 | 9826 | -  | 26 | sta | upstre | 0. | 0. | CHD1   | protei | 0 |
| \_76 | r5 | 2863 | 852.5 | 6842 |   | ne | 0908 | 2240 |    | 12 | rt  | am     | 0  | 0  |        | n\_cod |   |
| 5    |    |      |       |      |   |    |      |      |    |    |     |        |    |    |        | ing    |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 9826 | 98264 | 9826 | . | ge | 9826 | 9833 | +  | 22 | sta | overla | 0. | 0. | CTD-20 | lincRN | 1 |
| \_76 | r5 | 2863 | 852.5 | 6842 |   | ne | 4875 | 0717 |    |    | rt  | pStart | 5  | 03 | 07H13. | A      |   |
| 5    |    |      |       |      |   |    |      |      |    |    |     |        |    |    | 3      |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 9826 | 98264 | 9826 | . | ge | 9827 | 9827 | -  | 75 | sta | downst | 0. | 0. | Y\_RNA | misc\_ | 2 |
| \_76 | r5 | 2863 | 852.5 | 6842 |   | ne | 2342 | 2451 |    | 98 | rt  | ream   | 0  | 0  |        | RNA    |   |
| 5    |    |      |       |      |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| …    |    |      |       |      |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | ge | 1758 | 1758 | -  | 93 | sta | overla | 0. | 0. | NOP16  | protei | 0 |
| \_76 | r5 | 1450 | 6913. | 1931 |   | ne | 1094 | 1597 |    | 7  | rt  | pStart | 31 | 3  |        | n\_cod |   |
| 9    |    | 8    | 5     | 9    |   |    | 9    | 6    |    |    |     |        |    |    |        | ing    |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | NA | NA   | NA   | NA | NA | NA  | NA     | NA | NA | NA     | NA     | 1 |
| \_76 | r5 | 1450 | 6913. | 1931 |   |    |      |      |    |    |     |        |    |    |        |        |   |
| 9    |    | 8    | 5     | 9    |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| peak | ch | 1758 | 17581 | 1758 | . | NA | NA   | NA   | NA | NA | NA  | NA     | NA | NA | NA     | NA     | 2 |
| \_76 | r5 | 1450 | 6913. | 1931 |   |    |      |      |    |    |     |        |    |    |        |        |   |
| 9    |    | 8    | 5     | 9    |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+
| …    |    |      |       |      |   |    |      |      |    |    |     |        |    |    |        |        |   |
+------+----+------+-------+------+---+----+------+------+----+----+-----+--------+----+----+--------+--------+---+



Table 5: Uropa_BestperQuery_Hits for multiple queries. The column order is: peak_id, peak_chr, peak_start, peak_center, peak_end, peak_strand, feature, feat_start, feat_end, feat_strand, distance, feat_anchor, genomic_location, feat_ovl_peak, peak_ovl_feat, gene_name, gene_type, query

.. note:: 
	The BestperQuery_Hits is only generated if multiple queries are specified and the priority flag is set to FALSE! If this flag is TRUE, there will be only one valid query. There can be multiple valid annotations for one peak, but all based on one query.

Same as in the example with one query, peak_355 has no valid annotation at all and is represented as NA row in all produced output tables, correspond to Case 1. In the AllHits (Table 3) and BestperQuery_Hits (Table 5) there will be one NA row for each query, but in the FinalHits (Table 4) there will be only one NA row for all queries. 
The peak_356 has only for one query a valid annotation, this presented in AllHits, FinalHits, and BestperQuery_Hits conform to Case 2. In AllHits and BestperQuery_Hits there are additional NA rows for this peak for the other queries. 
For peak_765 there are valid annotations for all queries as displayed in the AllHits, representing Case 4. The best of them with the smalles distance is the annotation for the lincRNA, this annotation is displayed in the FinalHits. 
Because there is only one valid annotation for each query, all of this annotations are also displayed in the BestperQuery_Hits. 
This is different for peak_769, as described above this peaks equates to Case 3. With multiple queries, there will be additional NA rows for the invalid queries in the AllHits and BestperQuery_Hits. 

With multiple queries it is also possible to reformat the BestperQuery_Hits the a condensed format with the best per query annotations for each peak in one row.
A reformatted example for the BestperQuery_Hits of Table 5 is presented in Tables 6.1 and 6.2. Because this Table is very broad, it is splitted into two parts. 
The Reformatted_HitsperPeak represents all information for each peak in one row. Within this format the information for query 0 is always given at the first position, for query 1 at second positon and so on.

To receive this output format, the parameter **_-r_** has to be added to the command line call.

+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| pea | pea | pea | peak | pea |   | featu | feat\_s | feat\_e | feat | dis | feat\ | genomic\ | feat | peak | gene\_ | gene\_typ | qu |
| k\_ | k\_ | k\_ | \_ce | k\_ |   | re    | tart    | nd      | \_st | tan | _anch | _locatio | \_ov | \_ov | name   | e         | er |
| id  | chr | sta | nter | end |   |       |         |         | rand | ce  | or    | n        | l\_p | l\_f |        |           | y  |
|     |     | rt  |      |     |   |       |         |         |      |     |       |          | eak  | eat  |        |           |    |
+=====+=====+=====+======+=====+===+=======+=========+=========+======+=====+=======+==========+======+======+========+===========+====+
| …   |     |     |      |     |   |       |         |         |      |     |       |          |      |      |        |           |    |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| pea | chr | 792 | 7921 | 792 | . | NA,   | NA,NA,N | NA,NA,N | NA,N | NA, | NA,NA | NA,NA,NA | NA,N | NA,N | NA,NA, | NA,NA,    | 0, |
| k\_ | 15  | 115 | 7124 | 226 |   | NA,   | A       | A       | A,NA | NA, | ,NA   |          | A,NA | A,NA | NA     | NA        | 1, |
| 355 |     | 50  |      | 98  |   | NA    |         |         |      | NA  |       |          |      |      |        |           | 2  |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| pea | chr | 439 | 4390 | 439 | . | gene, | 4388106 | 4390461 | -,NA | 253 | start | overlapS | 0.57 | 0.09 | HNRNPF | protein\_ | 0, |
| k\_ | 10  | 025 | 4360 | 062 |   | NA,   | 5,NA,N  | 4,NA,N  | ,NA  | ,NA | NA,NA | tart,NA, | ,NA, | ,NA, | ,NA,NA | coding,NA | 1, |
| 356 |     | 16  | .5   | 05  |   | NA    | A       | A       | ,NA  | ,NA |       | NA       | NA   | A,NA |        | ,NA       | 2  |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| …   |     |     |      |     |   |       |         |         |      |     |       |          |      |      |        |           |    |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| pea | chr | 982 | 9826 | 982 | . | gene, | 9819090 | 9826224 | -,+, | 261 | start | upstream | 0,0. | 0,0. | CHD1,C | protein\_ | 0, |
| k\_ | 5   | 628 | 4852 | 668 |   | gene, | 8,98264 | 0,98330 | -    | 2,2 | t,sta | ,overlap | 5,0  | 3,0  | TD-200 | coding,li | 1, |
| 765 |     | 63  | .5   | 42  |   | gene  | 875,982 | 717,982 |      | 2,7 | rt,st | Start,do |      |      | 7H13.3 | ncRNA,mis | 2  |
|     |     |     |      |     |   |       | 72342   | 72451   |      | 598 | art   | wnstream |      |      | ,Y_RNA | cRNA      |    |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| …   |     |     |      |     |   |       |         |         |      |     |       |          |      |      |        |           |    |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| pea | chr | 175 | 1758 | 175 | . | gene, | 1758109 | 1758159 | -,NA | 937 | start | overlapS | 0.31 | 0.3, | NOP16, | protein\_ | 0, |
| k\_ | 5   | 814 | 1691 | 819 |   | NA,NA | 49,NA,N | 76,NA,N | ,NA  | ,NA | t,NA, | tart,NA, | ,NA  | NA,  | NA,NA  | coding,NA | 1, |
| 769 |     | 508 | 3.5  | 319 |   |       | A       | A       |      | ,NA | NA    | NA       | ,NA  | NA   |        | ,NA       | 2  |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+
| …   |     |     |      |     |   |       |         |         |      |     |       |          |      |      |        |           |    |
+-----+-----+-----+------+-----+---+-------+---------+---------+------+-----+-------+----------+------+------+--------+-----------+----+


Table 6: Uropa_Reformatted_HitsperPeak for multiple queries. 

Summary Vizualisation
---------------------
For every run there is also a summary output, vizualising the results for a global overview of the final annotation. Within this document one can find : 

A summery of the UROPA run: Used peak and annotation files, number of peaks and number of annotated peaks, specified queries, value of priority flag (Figure 1A). If not all queries annotated peaks, this is also mentioned.

**Graphs based on the 'FinalHits' output:**

- A density plot displaying the distance per feature across all queries (Figure 1B). 
- A pie chart illustrating the genomic locations of the peaks per annotated feature (Figure 1C).
- A barplot displaying the occurrence of the different features, if there is more than one feature assigned for peak annotation (not illustrated due to one feature in this example).

**Figure 1A-C would be the summary for the first UROPA run with only one query***

**Graphs based on the 'BestperQuery_Hits' output:**

- A distribution of the distances per feature per query are displayed in a histogram (Figure 1D).
- A pie chart illustrating the genomic locations of the peaks per annotated feature (not illustrated).
- A pairwise comparison among all queries is evaluated within a venn diagram, when more than one query is given in the config file (One pairwise comparison displayed in Figure 1E). 
- Chow Ruskey plot with comparison across all defined queries (for three to five annotation queries)(Figure 1F).

.. figure:: img/output-formats-summary.png

   Figure 1: Summary Example for queries as described above: (A) Summery of specified queries, used annotation and peak files, and how many peaks were present and annotated, (B) Distance density for all features based on FinalHits, (C) Pie Chart representing genomic location for each feature across FinalHits, (D) Distance per query per feature across BestperQuery_Hits, (E) Pairwise comparison across all queries displayed in Venn diagramms, (F) Chow Ruskey plot to compare all queries._
