About UROPA
===========
UROPA (‘Universal RObust Peak Annotator’) is a tool facilitating the analysis of next-generation sequencing methods for chromatin biology, 
like ChIP-seq or ATAC-seq. It is designed to annotate enrichted genomic regions (peaks) of interest, like peaks generated from any peak caller (e.g. `MACS2`_ or `MUSIC`_).

The annotation source is a GTF file, which provides the information of the genomic features to be used for annotation of the peaks. 
The peaks should be represented in BED file format. Annotation and peak files are specified in the configuration file. Furthermore, certain
parameters that define how peaks should be annotated can be adjusted (see :doc:`/config`). The output is given in easily-readable tab-delimited
tables with the corresponding annotation, as it is validated by the configuration file for each peak (see :doc:`/output`).

Without defining further parameters, the peaks will be annotated with a default annotation. To allow the
annotations to specific but flexible requirements, different parameters are available (see :doc:`/parameter`). Many usage examples are presented in the :doc:`/uropa-example`. Further exploration of those is advisable.

**Run UROPA**

To start the UROPA peak annotation, the minimal command is:

.. code:: bash

    uropa –i <config.json> –o <output_dir>

A template of the configuration file is available from our GitHub repository (see `sample_config.json`_). A quick overview about the usage and available parameters is displayed with

.. code:: bash

    uropa --help

.. _sample_config.json: https://github.molgen.mpg.de/loosolab/UROPA/blob/master/sample_config.json
.. _MUSIC: http://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0474-3
.. _MACS2: https://genomebiology.biomedcentral.com/articles/10.1186/gb-2008-9-9-r137