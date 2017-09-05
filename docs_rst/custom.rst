UROPA to GTF utility
====================
The GTF file is a common format used for annotation. UROPA accepts all GTF files downloaded from any online databases,              
such as UCSC, ensembl, or gencode. Additionally, custom GTF files can be used. 


The gencode v19 annotation GTF is illustrated in Table 7.1.                 

+------+--------+------+-------+-------+---+-----+---+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| chr1 | HAVANA | gene | 11869 | 14412 | . | \+\ | . | gene_id "ENSG00000223972" ; transcript_id "ENSG00000223972.4";gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1";transcript_type "pseudogene";transcript_status "KNOWN";transcript_name "DDX11L1"; level 2; havana_gene "OTTHUMG00000000961.2"; |
+------+--------+------+-------+-------+---+-----+---+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ...  |        |      |       |       |   |     |   |                                                                                                                                                                                                                                                               |
+------+--------+------+-------+-------+---+-----+---+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Table 7.1:** First row of gencode v19 GTF file

The uropa2gtf-tool transforms annotation files that are not in GTF format.
Files for annotation can be generated for instance by the `UCSC Table Browser`_ , or many other data bases.
For the conversion, the input annotation file needs to have a header, and there need to be columns with information about the
location: 'chr', 'start', and 'end' . Additionally, the file should be tab separated. 

Another requirement is a file name without dots. 

For example, if transcription factor binding sites (tfbs) from the UCSC table browser were downloaded, the name of the file should be the
name of the table: 'wgEncodeAwgTfbsBroadHuvecCtcfUniPk.txt'. The file name will be used in the attribute column. 

There are two variations of the GTF file generator:

1.	One file should be converted and used for annotation. The GTF file keeps the same as the base file name. 
2.	Several files should be used for annotation. In this case the input should be a folder with all annotation files included (but no others).  
	The files will be converted one by one; additionally one merged GTF file (called uropa2gtf_'basename of the input dir'.gtf) will be created. 
	For the merged file, the explicit file names are important for distinguishing the annotated features. 

The generated files will be stored in the same directory as the input file is located. 

Beside the mandatory input, there are three optional arguments that can be given for the transformation. Those are the source, feature and number of threads.     
The usage of this utility is very simple:

.. code:: bash

	uropa2gtf.R -i input
	
This is the basic usage, by using further parameters, further features can be specified with

.. code:: bash

	uropa2gtf.R -i input -s yourSource -f yourFeature -t number-threads
	e.g.
	uropa2gtf.R -i wgEncodeAwgTfbsBroadHuvecCtcfUniPk.txt -s ucsc -f tfbs -t 5
	

The two arguments source and feature are used for the GTF reformatting itself. The argument threads can be used if multiprocessing should be used.   
There should be no spaces between the character and the equal sign when using the parameters in the command line call. 

If optional arguments are given, they will overwrite information from the input file(s).
Within the transformation, the input file is checked for information that is necessary for the GTF file format, like chr, start, end, strand, and others.      
If the information is present in the input file, it will be adopted to the new GTF file.                       
The optional arguments are used in the GTF file for the corresponding columns, if one optional argument is not given and this information is also not present in the input file,       
the column will be filled with *undefined*. For other information that is not present in the input file, the column will be filled with dots.          
All additional columns presented in the input file will be merged in the attributes column of the new GTF file. All that information can be shown as annotation specification using the ``show.attribute`` key using UROPA.
Furthermore, these are the attributes which can be filtered for specific values with the two linked keys ``filter.attribute`` and ``attribute.value``.

The custom GTF transformation is useful if the peaks should not be annotated to a gene, but for example to known tfbs or other regulatory elements.            
For instance, this is handy for an ATAC-seq peak annotation.  

+------+-------+------------+----------+------+-------+--------+-------------+--------+---------+------+
| #bin | chrom | chromStart | chromEnd | name | score | strand | signalValue | pValue | qValue  | peak |
+------+-------+------------+----------+------+-------+--------+-------------+--------+---------+------+
| 74   | chr1  | 1310465    | 1310835  | .    | 244   | .      | 372.141     | -1     | 482.217 | 185  |
+------+-------+------------+----------+------+-------+--------+-------------+--------+---------+------+
| 76   | chr1  | 3407792    | 3408060  | .    | 1000  | .      | 178.305     | -1     | 482.214 | 129  |
+------+-------+------------+----------+------+-------+--------+-------------+--------+---------+------+
| ...  |       |            |          |      |       |        |             |        |         |      |
+------+-------+------------+----------+------+-------+--------+-------------+--------+---------+------+

**Table 7.2:** Downloaded table from UCSC Table Browser (wgEncodeAwgTfbsBroadHuvecCtcfUniPk) for CTCF transcription factor from Uniform TFBS track.

After transformation with ``-f tfbs`` and ``-s ucsc``, the GTF format annotation file will look as displayed in Table 7.3.  

+------+------+------+---------+---------+------+---+---+------------------------------------------------------------------------------------------------------------+
| chr1 | ucsc | tfbs | 1310465 | 1310835 | 244  | . | . | bin 74; signalvalue 372.141; pvalue -1; qvalue 482.217; peak 185; table wgEncodeAwgTfbsBroadHuvecCtcfUniPk |
+------+------+------+---------+---------+------+---+---+------------------------------------------------------------------------------------------------------------+
| chr1 | ucsc | tfbs | 3407792 | 3408060 | 1000 | . | . | bin 76; signalvalue 178.305; pvalue -1; qvalue 482.217; peak 129; table wgEncodeAwgTfbsBroadHuvecCtcfUniPk |
+------+------+------+---------+---------+------+---+---+------------------------------------------------------------------------------------------------------------+

**Table 7.3:** GTF file download from UCSC table browser for wgEncodeAwgTfbsBroadHuvecCtcfUniPk


.. _UCSC Table Browser: https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=502498195_cPIoMqXhw14ApzQemlpIvSHD9o8D