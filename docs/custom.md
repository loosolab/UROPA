The GTF file is a very common format used for annotation. UROPA accepts all GTF files downloaded from any online databases,              
such as UCSC, ensembl, GENCODE. The file fromat is well-explained by [Ensembl](http://www.ensembl.org/info/website/upload/gff.html )       
The Gencode v19 annotation GTF looks for example like shown in Table 1.                 
 
|    |      |          |     |     | | | |                                                                                                                                                                                                                                                              | 
|----|------|----------|-----|-----|-|-|-|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
|chr1|HAVANA|gene      |11869|14412|.|+|.|gene_id "ENSG00000223972"; transcript_id "ENSG00000223972.4"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "pseudogene";transcript_status "KNOWN";transcript_name "DDX11L1"; level 2; havana_gene "OTTHUMG00000000961.2";| 
|...                                                                                                                                                                                                                                                                                                    | 

_Table 1: first row of gencode v19 GTF file, the columns are: chr, source, feature, start, end, score, strand, frame, and attributes. (Left out: description header)_

For further extending the utility of UROPA, there is the UROPAtoGTF tool which transforms annotation files that are not in this format.
Files for annotation can be provided by the [UCSC Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables), or many more data bases.   
For the internal convertion, the input annotation file needs to have a header, and there need to be columns with information about the location: 'chr', 'start', and 'end' .
Additionally, the file should be tab separated. Another requirement for the transformation is that the file name should be explicit for the file content and does not contain dots.
For example, if transcription factor binding sites (tfbs) from UCSC table browser were downloaded, the name of the file could be the name of the table 'wgEncodeAwgTfbsBroadHuvecCtcfUniPk.txt'. 
The file name will be one information in the attribute column. 
There are two variations of the GTF file generator:

1.	One file should be converted and used for annotation. 
2.	Several files should be used for annotation. In this case the input should be a folder with all files included (but no others).  
	The files will be converted one by one; additionally one merged GTF file (called UROPAtoGTF_merged.GTF) will be created. 
	For the merged file, the explicit file names are important for distinguishing the annotated features. 

The generated files will be stored in the same directory as the input file is located. 
Furthermore, there are two optional arguments that can be given for the transformation. Those are source and feature.     
If an optional argument will be used, it should be used with source=yourSource and feature=yourFeature, e.g. source=UCSC feature=tfbs.    
There should be no spaces between the character and the equal sign. If optional arguments are given, they will overwrite information from the input file(s).
If only one input file was given, the GTF file version of this file will be used as annotation file.        
If more input files were present, the merged file will be used as annotation file. 
Whitin the transformation, the input file is checked for information that is necessary for the GTF file format, like chr, start, end, strand, and more.      
If the information is present in the input file, it will be adopted to the GTF file.             
For the chromosome column it checks the format, if the chromosome is presented by 1, 2 etc., it will be reformatted to chr1, chr2 etc. format.          
The optional arguments are used in the GTF file for the corresponding column, if one optional argument is not given and this information is also not present in the input file,       
the column will be filled with undefined. For other information that is not present in the input file, the column will be filled with dots.          
All additional columns presented in the input file will be merged in the attributes column.  All that information can be represented in the UROPA output file by the key 'attributes'. 

The custom GTF transformation is useful if the peaks should not be annotated to a gene, but for example to known tfbs or other regulatory elements.            
For instance, this is handy for an ATAC-seq peak annotation.  

#Transformation Example
In Table 2 the CTCF transcription factor table from UCSC is shown. This should be part of the annotation for the ATAC-seq peaks.

| #bin | chrom | chromStart | chromEnd | name | score | strand | signalValue | pValue | qValue  | peak | 
|------|-------|------------|----------|------|-------|--------|-------------|--------|---------|------| 
| 74   | chr1  | 1310465    | 1310835  | .    | 244   | .      | 382.141     | -1     | 482.217 | 185  | 
| 76   | chr1  | 3407792    | 3408060  | .    | 1000  | .      | 178.305     | -1     | 482.217 | 129  | 
|...   |       |            |          |      |       |        |             |        |         |      | 

Table 2: Downloaded table from [UCSC Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables) (wgEncodeAwgTfbsBroadHuvecCtcfUniPk) for CTCF transcription factor from Uniform TFBS track.

After transformation with feature=tfbs but without given source, the GTF format annotation file will look as displayed in Table 3.  

|      |           |      |         |         |      |   |   |                                                                                                        | 
|------|-----------|------|---------|---------|------|---|---|--------------------------------------------------------------------------------------------------------| 
| chr1 | undefined | tfbs | 1310465 | 1310835 | 244  | . | . | signalValue  382.141 ; pValue -1 ; qValue 4.82217 ; peak 185; table wgEncodeAwgTfbsBroadHuvecCtcfUniPk | 
| chr1 | undefined | tfbs | 3407792 | 3408060 | 1000 | . | . | signalValue 178.305 ; pValue -1 ; qValue 4.82217 ; peak 129; table wgEncodeAwgTfbsBroadHuvecCtcfUniPk  | 

Table 3: Internal transformation to GTF file format of CTCF table from UCSC.

#Advantage of UROPA internal GTF transformation vs. download the tables in GTF file format
The UCSC table browser also supports GTF file format. But whithin this GTF file, not the information about the original peak for this tfbs is disblayed,      
only the exon in which the peak is located is displayed. Additionally for this example, in the attribute column,           
there are empty information about 'gene_id' and information about peak, pValue und signalValue are lost. 
An example of the GTF output from UCSC table browser is shown in Table 4.

|      |                                         |      |         |         |           | | |                                      |
|------|-----------------------------------------|------|---------|---------|-----------|-|-|--------------------------------------| 
| chr1 | hg19_wgEncodeAwgTfbsBroadHuvecCtcfUniPk | exon | 1310466 | 1310835 | 244.000000|.|.| gene_id "."; transcript_id ".";      | 
| chr1 | hg19_wgEncodeAwgTfbsBroadHuvecCtcfUniPk | exon | 1334906 | 1334997 | 630.000000|.|.| gene_id "."; transcript_id "._dup1"; | 


Table 4: GTF file download from UCSC table browser for wgEncodeAwgTfbsBroadHuvecCtcfUniPk

The major problem with the UCSC GTF file is that in this the exon location and not the tfbs location is displayed.         
That means, the peaks that should be annotated cannot be annotated for them tfbs itself. That is why the tables should be downloaded with the output format      
'all fields from selected table' or with 'select fields from primary and related tabs'. 

