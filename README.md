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
-  Different easily-readable output tables (allhits, finalfits, besthits).
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files

Documentation
--------------
A detailed description of how to apply UROPA to your data can be found [here](http://uropa-manual.readthedocs.io/).

Installation and Command-line usage
------------------------------------
Make sure all prerequisites are met:

- [Python](http://continuum.io/downloads) 
	- download Anaconda for Linux version Python 2.7 to direction where python should be installed
	- run ```bash Anaconda2-4.3.0-Linux-x86_64.sh``` 
	- Answer the question "Do you wish the installer to prepend the Anaconda2 install location to PATH in your /home/.../.bashrc ?" with yes 
		OR do ```PATH=dir/to/python_anaconda:$PATH``` after installation process
	- run ```conda install -c bioconda pysam```
- [R/Rscript](http://www.r-project.org/) (v3.3.0 or higher; follow instructions on url)
	- install required packages step by step: 
	```bash
	install.packages(c("ggplot2", "devtools", "gplots", "gridExtra", "jsonlite", "VennDiagram", "getopt"))
	source("https://bioconductor.org/biocLite.R")
	biocLite(c("RBGL","graph"))
	# to install the last required package, devtools has to be loaded to use the install from github function
	library(devtools)
	install_github("jenzopr/Vennerable")
	```
- [Git](https://git-scm.com/): run ```bash sudo apt-get install git``` 

### Install UROPA locally

```bash
git clone https://github.molgen.mpg.de/loosolab/UROPA.git
export PATH=$PATH:dir/to/uropa
```

```bash                        
Usage: uropa.py [options]          

Available options:

	-h, --help             	print this help message and further details on the configuration file
        -i, --input            	filename of configuration file [mandatory]
        -p, --prefix           	prefix for output files, can include subdirectories [basename of --input]
        -r, --reformat         	create an additional compact and line-reduced table as result file
        -s, --summary          	additional visualisation of results in graphical format will be created
        -t n, --threads n      	multiprocessed run: n = number of threads to run annotation process
        -add-comments          	show comment lines in output files explaining the columns
        -l, --log              	log file name for messages and warnings
        -d, --debug            	print verbose messages (for debugging purposes)
        -v, --version          	print the version and exit
```

How to cite
-----------

Kondili M, Fust A, Preussner J, Kuenne C, Braun T, and Looso M. UROPA: a tool for Universal RObust Peak Annotation. *Scientific Reports* **7** (2017), doi: [10.1038/s41598-017-02464-y](https://www.nature.com/articles/s41598-017-02464-y)

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
