UROPA - Universal RObust Peak Annotator
=======================================

UROPA (‘Universal RObust Peak Annotator’) is a command line based tool, intended for genomic region
annotation. Based on a configuration file, different target features can be prioritized with multiple integrated queries. 
These can be sensitive for feature type, distance, strand specificity, feature attributes (eg. protein_coding) or the anchor position relative to the feature. 
UROPA can incorporate reference annotation files (GTF) from different sources, like Gencode, Ensembl, or RefSeq, 
as well as custom reference files produced by the user.

Features
--------
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

Documentation
--------------
A detailed description of how to apply UROPA to your data can be found [here](uropa2.readthedocs.io).

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
	
	- i, --input		configuration file
	- o, --output		output: folder for results and part of the output files in one
	- h, --help			this help message and further information, e.g. about the configuration file
	- v, --version		print the version and exit 
	- d, --debug		print verbose messages
	- l, --log			log file for messages and warnings 
	- r, --reformat		additional output file: a more compact line-reduced table of BestperQuery_Hits
	- s, --summary		additional output file: visualisation of results in graphical format
	-t n, --threads n	multiprocessed run: n = number of threads to run annotation process
```

How to cite
-----------

tba

Contribute
----------

* Source Code [here](https://github.molgen.mpg.de/loosolab/UROPA)
* Issue Tracker [here](https://github.molgen.mpg.de/loosolab/UROPA/issues)

Support
-------

If you have any questions please feel free to contact Maria Kondili (maria.kondili@mpi-bn.mpg.de).

License
-------

The project is licensed under the MIT License.
