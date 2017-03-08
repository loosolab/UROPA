Installation
============

Prerequisites
-----------------
For running UROPA locally, the following prerequisites have to be met:

- `Python`_, v2.7 
	- download Anaconda for Linux version Python 2.7 to direction where python should be installed
	- run ``bash Anaconda2-4.3.0-Linux-x86_64.sh``
	- Answer the question "Do you wish the installer to prepend the Anaconda2 install location to PATH in your /home/.../.bashrc ?" with yes OR do ``PATH=dir/to/python_anaconda:$PATH`` after th installation process has finished
	- run ``conda install -c bioconda pysam``
	- if you are NOT using the anaconda version of python 2, the packages `pysam`_ and `numpy`_ can be installed with ``pip install pysam numpy``
- `R/Rscript`_, v3.3.0 or higher (follow the instructions on url)
	Install packages:
	
	- ``install.packages(c("ggplot2", "devtools", "gplots", "gridExtra", "jsonlite", "VennDiagram", "snow"))``
	
	## choose mirrow
	
	- ``source("https://bioconductor.org/biocLite.R")``
	- ``biocLite(c("RBGL","graph"))``
	- ``library(devtools)``
	- ``install_github("jenzopr/Vennerable")``
	- further package infos can be found at `CRAN`_
- `git`_ with ``bash sudo apt-get install git``

UROPA
-----
UROPA itself can be installed by simply cloning the Github library and adding the target folder to the system environment variable.

.. code:: bash

	git clone https://github.molgen.mpg.de/loosolab/UROPA
	export PATH=$PATH:dir/to/uropa
		


.. _R/Rscript: http://www.r-project.org/
.. _Python: http://continuum.io/downloads
.. _Anaconda: http://continuum.io/downloads
.. _git: https://git-scm.com/
.. _numpy: http://www.numpy.org
.. _pysam: https://pysam.readthedocs.io/en/latest/index.html
.. _CRAN: https://cran.r-project.org/web/packages/
