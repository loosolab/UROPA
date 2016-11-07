Installation
============

For running UROPA locally, the following prerequisites have to be met:

- `R/Rscript`_, v3.3.0 or higher, follow instructions on url
- `Python`_ , v2.7.8-anaconda-2.1.0
with ``bash Anaconda2-4.2.0-Linux-x86_64.sh`` and ``PATH=dir/to/python_anaconda:$PATH``

- `htslib`_ 1.3.2 or higher, follow instructions on url

Required packages
-----------------

For python
~~~~~~~~~~
- `numpy`_
- `pysam`_

Install with ``pip install pysam numpy``

For R
~~~~~
- `ggplot2`_
To install R packages hosted by CRAN start R and then type ``install.packages("ggplot2")``. 
After choosing a downloading mirrow, the package will be downloaded and installed. 
To use the package in R it has to be loaded with ``library("ggplot2")``, but within UROPA this will be done automatically.
	
- `gplots`_
- `gridExtra`_ 
- `jsonlite`_ 
- `VennDiagram`_ 
- Vennerable
This package needs a couple of BioConductor packages. To install those start R and type ``source("https://bioconductor.org/biocLite.R")`` and ``biocLite(c("RBGL","graph"))``.
Additionally, the package ``devtools`` is needed and should be installed from CRAN (``install.packages("devtools")``).
Afterwards the package can be installed with ``install_github("jenzopr/Vennerable")`` and loaded with ``library(Vennerable)``. But again this will be done automatically within UROPA.

- If multiprocessing should be available: `snow`_ 


Install UROPA locally
---------------------

Run:

.. code:: bash

	git clone https://github.molgen.mpg.de/loosolab/UROPA
	export PATH=$PATH:dir/to/uropa
		
Now you can run uropa with the specified configuration file and the annotation database of interest. 

.. _R/Rscript: http://www.r-project.org/
.. _Python: http://continuum.io/downloads
.. _htslib: http://www.htslib.org/download/
.. _numpy: http://www.numpy.org
.. _pysam: https://pysam.readthedocs.io/en/latest/index.html
.. _ggplot2: https://cran.r-project.org/web/packages/ggplot2/index.html
.. _gplots: https://cran.r-project.org/web/packages/gplots/index.html
.. _gridExtra: https://cran.r-project.org/web/packages/gridExtra/index.html
.. _jsonlite: https://cran.r-project.org/web/packages/jsonlite/index.html
.. _VennDiagram: https://cran.r-project.org/web/packages/VennDiagram/index.html
.. _snow: https://cran.r-project.org/web/packages/snow/index.html