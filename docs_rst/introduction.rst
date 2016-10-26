About UROPA
===========
UROPA (‘Universal RObust Peak Annotator’) is a tool facilitating the
analysis of next-generation sequencing methods for chromatin biology,
like ChIP-seq or ATAC-seq. It is designed to annotate enrichted genomic
regions (peaks) of interest generated from any peak caller (e.g. MACS2,
MUSIC, FindPeaks, CisGenome, PeakSeq).

The annotation source is a GTF file, which provides the information of
the genomic features to be used for annotation of the peaks. The peaks
should be represented in BED file format. Annotation and peak files
have to be specified in the configuration file. Furthermore, certain
parameters that define how peaks should be annotated can be adjusted (see `Configuration file`_). 
The output is given in easily-readable tab-delimited
tables with the corresponding annotation, as it is validated by the
configuration file for each peak (see `Output tables`_).

Without defining further parameters, the peaks will be annotated with a default annotation. To adjust the
annotations to specific but flexible requirements, the different parameters of
the config file should be used. Examples of usage are presented in
the `Application Examples <uropa-example.html>`_. Further exploration is suggested.


Advantages of UROPA
-------------------
-  Simple usage: No programming
-  Utilization of all available GTF files as annotation database
-  Annotation with default values
-  Detect the most appropriate annotation with flexible parameter keys that allow
   robustness and simple customization, such as
   -  feature type
   -  feature anchor
   -  feature direction relative to peak location
   -  filter for attribute values, e.g. “protein\_coding”
   -  strand specificity
-  One run with multiple sets of parameters by multiple queries
-  Graduated annotation due to priorization
-  Different easily-readable output tables (AllHits, FinalHits,
   BestperQuery\_Hits).
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files


Run UROPA
---------
To start the UROPA peak annotation, the minimal command is:

.. code:: bash

    uropa –i <config.json> –o <output_dir>

A template of the file config.json is prepared in the working directory
when downloading UROPA, named “a\_config\_example.json”. A quick
overview about UROPA usage is displayed with * **uropa -h** *.