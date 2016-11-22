UROPA - Universal RObust Peak Annotator
=======================================

UROPA (‘Universal RObust Peak Annotator’) is a command line based tool, intended for genomic region
annotation. Based on a configuration file, different target features can be prioritized with multiple integrated queries. 
These can be sensitive for feature type, distance, strand specificity, feature attributes (eg. protein_coding) or the anchor position relative to the feature. 
UROPA can incorporate reference annotation files (GTF) from different sources, like Gencode, Ensembl, or RefSeq, 
as well as custom reference files produced by the user.

Features
--------

-  Detect the most appropriate annotation with flexible parameter keys that allow
   robustness and simple customization, such as
   
   -  feature type
   -  feature anchor
   -  feature direction relative to peak location
   -  filter for attribute values, e.g. “protein\_coding”
   -  strand specificity

-  Utilization of all available GTF files as annotation database
-  One run with variable sets of parameters by multiple queries
-  Graduated annotation due to priorization
-  Different easily-readable output tables (AllHits, FinalHits, BestperQuery\_Hits).
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files

Documentation
--------------
A detailed description of how to apply UROPA to your data can be found [here](http://uropa2.readthedocs.io/en/latest/).

Installation and Command-line usage
------------------------------------
Make sure all prerequisites are met:

- [R/Rscript](http://www.r-project.org/)
- [Python](http://continuum.io/downloads)

Install UROPA locally by running:

```bash
git clone https://github.molgen.mpg.de/loosolab/UROPA.git
export PATH=$PATH:dir/to/uropa/src
```

```bash                        
Usage: uropa [options]          

Available options:
	
	- h, --help             print this help message and further details on the configuration file
        - i, --input            filename of configuration file
        - o, --output           directory for results and prefix of the output file name
        - r, --reformat         create an additional compact and line-reduced table as result file
        - s, --summary          filename of additional visualisation of results in graphical format
        - t n, --threads n      multiprocessed run: n = number of threads to run annotation process
        --no-comment            do not show comment lines in output files
        - l, --log              log file name for messages and warnings
        - d, --debug            print verbose messages (for debugging purposes)
        - v, --version          print the version and exit
```

How to cite
-----------

Kondili M, Fust A, Preussner J, Kuenne C and Looso M. UROPA: a tool for Universal RObust Peak Annotation. *(in preparation)*

Contribute
----------

* Source Code [here](https://github.molgen.mpg.de/loosolab/UROPA)
* Issue Tracker [here](https://github.molgen.mpg.de/loosolab/UROPA/issues)

Support
-------

If you have any questions please feel free to contact Mario Looso (mario.looso@mpi-bn.mpg.de).

License
-------

The project is licensed under the MIT License.
