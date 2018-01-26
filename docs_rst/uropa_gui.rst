UROPA GUI
==========

**A Web Platform for genomic region annotation**
 
The annotation of genomic ranges such as peaks resulting from ChIP-seq/ATAC-seq or other techniques represents a fundamental task of bioinformatics analysis with crucial impact on many downstream analyses. In our previous work, we introduced the Universal Robust Peak Annotator (UROPA), a flexible command line based tool which considerably extends the functionality of existing annotation software. In order to reduce the complexity for biologists and clinicians, we have implemented an intuitive web-based graphical user interface (GUI) and fully functional service platform for UROPA. This extension will empower all users to generate annotations for regions of interest interactively.

Features
---------

* **Input**: BED file of peaks or other genomic regions
* **Reference**: GTF file of desired target features (e.g. genes, transcripts, probes, repeats, ...);                                                        source = Gencode/Ensembl (102 organisms included) or custom upload
* **Association rules**: VERY diverse and easily combinable to a complex ruleset (see :doc:`/config`)
* **Persistence**: Unique identifier is created on the server and results will remain available temporarily using the respective link
* **Hosted**: Either online on our web server or as a local R Shiny installation

Availability and Implementation
-------------------------------

The open source UROPA GUI server was implemented in R Shiny and Python and is available from `UROPA_GUI`_ .
Please make sure to check `loosolab`_ for a comprehensive overview of all our projects and implemented tools.

Try UROPA GUI
--------------

The `UROPA_GUI`_ contains all necessary data to quickly sample the capabilities of UROPA GUI.
*  **UROPA GUI user guide**: Stepwise tutorial.

* **Example data**: The following demo GTF and BED files are available on the server.                                                               Homo_sapiens.hg19.GRCh37.75_genes_v2.gft -> `Human GTF` file with reference genes                                   ENCFF001VFA.pol2.sub.bed -> `POLR2A`_ ChIP-seq experiment (14989 peaks)

.. note::  It is mandatory to select ``filter.attribute`` before ``attribute.value``. Depending on the GTF file, it might take some time for the ``attribute.value`` to be loaded. Please be patient!

How to cite
------------

* Kondili M, Fust A, Preussner J, Kuenne C, Braun T, and Looso M. UROPA: a tool for Universal RObust Peak Annotation. Scientific Reports 7 (2017), doi: https://www.nature.com/articles/s41598-017-02464-y
* Hendrik Schultheis, Jens Preussner, Annika Fust, Mette Bentsen, Carsten Kuenne, Mario Looso: UROPA: A Web Platform for genomic region annotation

License
-------

This project is licensed under the MIT license.

.. _UROPA_GUI: http://loosolab.mpi-bn.mpg.de/apps/UROPA
.. _loosolab: http://loosolab.mpi-bn.mpg.de/
.. _POLR2A: https://www.encodeproject.org/experiments/ENCSR000EAD/
.. _Human GTF: ftp://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/ 