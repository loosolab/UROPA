Universal RObust Peak Annotator
=======================================

[![Anaconda-Server Badge](https://img.shields.io/badge/Install%20with-conda-green.svg?style=plastic&logoWidth=40)](https://conda.anaconda.org/bioconda) [![Docker Badge](https://img.shields.io/badge/Container-ready-green.svg?style=plastic&logoWidth=40)](http://biocontainers.pro/registry/#/) [![PyPI Version](https://img.shields.io/pypi/v/uropa.svg?style=plastic)](https://pypi.org/project/uropa/)

The **Universal RObust Peak Annotator** (UROPA) is a command line based tool, intended for genomic region
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

### Conda package manager

We recommend to install UROPA using the conda package manager. Make sure to have `conda` installed, e.g. via

- [Miniconda](https://conda.io/miniconda.html)
	- download the Miniconda installer for **Python 3**
	- run ```bash Miniconda3-latest-Linux-x86_64.sh``` to install Miniconda
	- Answer the question "Do you wish the installer to prepend the Miniconda install location to PATH in your /home/.../.bashrc ?" with yes
		OR do ```PATH=dir/to/miniconda3:$PATH``` after installation process

The UROPA installation is now as easy as 

```conda create --name uropa```

```conda activate uropa```

```conda install python uropa```.

### Biocontainers / Docker

If you have a running [Docker](docker.com) environment, you can pull a biocontainer with UROPA and all dependencies via

-	`docker pull quay.io/biocontainers/uropa:latest_tag` using the latest tag from the [taglist](https://quay.io/repository/biocontainers/uropa?tab=tags), e.g. `1.2.1--py27r3.3.2_0`
-	`docker pull loosolab/uropa`

### Installation from source

You can also install UROPA from the source PyPI package. Note that this comes without the R dependencies for auxillary scripts:

`pip install uropa`

To fulfill all other dependencies, follow the instructions below:

- [R/Rscript](http://www.r-project.org/) (v3.3.0 or higher; follow instructions on url)
	- install required packages step by step:
	```bash
	install.packages(c("ggplot2", "devtools", "gplots", "gridExtra", "jsonlite", "VennDiagram", "getopt", "tidyr", "UpSetR"))
	source("https://bioconductor.org/biocLite.R")
	biocLite(c("RBGL", "graph"))
  ```

In order to plot the Chow-Ruskey plot with uropa_summary.R, install the modified Vennerable package from our fork:

```
library(devtools)
install_github("jenzopr/Vennerable")
```

### Usage

To effectively use UROPA, make yourself familiar with the command-line options:

## Command-line usage

```bash
$ uropa                   
Usage: uropa [options]          

optional arguments:
  -h, --help                       show this help message and exit

Arguments for one query:
  -b , --bed                       Filename of .bed-file to annotate
  -g , --gtf                       Filename of .gtf-file with features
  --feature [ [ ...]]              Feature for annotation
  --feature_anchor [ [ ...]]       Feature anchor to annotate to
  --distance [ [ ...]]             Maximum permitted distance from feature (1 or 2
                                   arguments)
  --strand [ [ ...]]               Desired strand of annotated feature relative to peak
  --relative_location [ [ ...]]    Peak locaion relative to feature location
  --internals                      Set minimum overlap fraction for internal feature
                                   annotations. 0 equates to internals=False and 1 equates
                                   to internals=True. Default is False.
  --filter_attribute               Filter on 9th column of GTF
  --attribute_values [ [ ...]]     Value(s) of attribute corresponding to
                                   --filter_attribute
  --show_attributes [ [ ...]]      A list of attributes to show in output

Multi-query configuration file:
  -i config.json, --input config.json
                                   Filename of configuration file (keys in this file
                                   overwrite command-line arguments about query)

Additional arguments:
  -p , --prefix                    Prefix for result file names (defaults to basename of
                                   .bed-file)
  -o , --outdir                    Output directory for output files (default: current
                                   dir)
  -s, --summary                    Filename of additional visualisation of results in
                                   graphical format
  -t n, --threads n                Multiprocessed run: n = number of threads to run
                                   annotation process
  -l uropa.log, --log uropa.log    Log file name for messages and warnings (default: log
                                   is written to stdout)
  -d, --debug                      Print verbose messages (for debugging)
  -v, --version                    Prints the version and exits

```

## Biocontainer usage

Running UROPA from a docker container can be done using the following command:

```bash
sudo docker run --rm -v <path-to-input-files-on-HOST>:<path-to-container-mnt> UROPA:LATEST uropa <UROPA-Paramters> -p <path-to-container-mnt>/'your-file-prefix'
```

*-v parameter mounts a HOST folder into your docker CONTAINER. This folder should contain the input files for UROPA and also the result files will be stored here. No files will be stored in the container!*

*--rm removes/closes the container after the run*

Make sure to use the uropa -p option specifying the output directory and prefix, otherwise results are lost in the container environment.

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
