About UROPA
===========
UROPA (‘Universal RObust Peak Annotator’)  is a command line based tool, intended for universal genomic range (e.g. peaks) annotation.
Based on a configuration file, different target features can be prioritized with multiple integrated queries. 
These can be sensitive for feature type, distance, strand specificity, feature attributes (eg. protein_coding) or anchor position relative to the feature. 
UROPA can incorporate reference annotation files (GTF) from different sources, as well as custom reference annotation files produced
by the user. Statistics and plots transparently summarize the annotation process. UROPA is implemented in Python and R.

- The user provides a reference annotation file in GTF format 
- The user provides ranges/peaks of interest in BED file format
- The user provides a configuration file in JavaScript Object Notation (JSON) format

The tool permits linkage of individual queries including prioritization (see :doc:`/config`).
Arbitrary features in the reference annotation file can be addressed in a granular way (see :doc:`/parameter`).
Filtering on additional annotation columns in the reference annotation file is supported. 
UROPA generates publication ready graphical statistics. The output is given in easily-readable tab-delimited tables (see :doc:`/output`).

Many usage examples are presented in the :doc:`/uropa-example`.

**Run UROPA**

To start the UROPA peak annotation, the minimal command is:

.. code:: bash

    uropa.py –i <config.json>

A template of the configuration file is available from our GitHub repository (see `sample_config.json`_). An overview about the usage and available parameters is displayed with

.. code:: bash

    uropa.py --help

.. _sample_config.json: https://github.molgen.mpg.de/loosolab/UROPA/blob/master/sample_config.json
