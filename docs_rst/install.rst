Installation
============

Prerequisites
-----------------
For running UROPA locally, the following prerequisites have to be met:

- `Python`_, v2.7 (packages: numpy, sampy)
- `R/Rscript`_, v3.3.0 or higher (packages: devtools, ggplot2, gplots, gridExtra, jsonlite, RBGL, graph, VennDiagram, Vennerable, snow)
- `htslib`_ 1.3.2 or higher

Instructions
-----------------

Python
~~~~~~~~~~
As numpy and sampy packages can be taxing to install in Python, we recommend the usage of the `Anaconda` distribution instead (v2.7.8-anaconda-2.1.0 or higher). Install with eg. ``bash Anaconda2-4.2.0-Linux-x86_64.sh`` and include the path in the environment variable ``PATH=dir/to/python_anaconda:$PATH``.

Using standard Python 2.7, the packages can be installed with ``pip install pysam numpy``.

R
~~~~~
The following packages are hosted by CRAN and can be installed with the syntax ``install.packages("packagename")``.

- `devtools`_
- `ggplot2`_
- `gplots`_
- `gridExtra`_ 
- `jsonlite`_ 
- `VennDiagram`_ 
- `snow`_ 

The RBGL and graph packages are hosted by BioConductor. To install those start R and type ``source("https://bioconductor.org/biocLite.R")`` and ``biocLite(c("RBGL","graph"))``.

Vennerable has to be installed with ``install_github("jenzopr/Vennerable")``.

UROPA
---------------------

Run:

.. code:: bash

	git clone https://github.molgen.mpg.de/loosolab/UROPA
	export PATH=$PATH:dir/to/uropa
		
Now you can run uropa with the specified configuration file and the annotation database of interest. 

.. _R/Rscript: http://www.r-project.org/
.. _Python: http://continuum.io/downloads
.. _Anaconda: http://continuum.io/downloads
.. _htslib: http://www.htslib.org/download/
.. _numpy: http://www.numpy.org
.. _pysam: https://pysam.readthedocs.io/en/latest/index.html
.. _ggplot2: https://cran.r-project.org/web/packages/ggplot2/index.html
.. _gplots: https://cran.r-project.org/web/packages/gplots/index.html
.. _gridExtra: https://cran.r-project.org/web/packages/gridExtra/index.html
.. _jsonlite: https://cran.r-project.org/web/packages/jsonlite/index.html
.. _VennDiagram: https://cran.r-project.org/web/packages/VennDiagram/index.html
.. _snow: https://cran.r-project.org/web/packages/snow/index.html
.. _devtools: https://cran.r-project.org/web/packages/devtools/
