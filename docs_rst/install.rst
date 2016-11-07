Installation
============

For running UROPA locally, the following prerequisites have to be met:

- `R/Rscript`_, v3.3.0 or higher
install with:

.. code:: bash
	
	sudo apt-get update
	sudo apt-get install r-base

- `Python`_ , v2.7.8-anaconda-2.1.0
- `htslib`_ 1.3.2 or higher

Required packages
-----------------

For python
~~~~~~~~~~
- `numpy`_
- `pysam`_


For R
~~~~~
- `ggplot2`_
To install R packages hosted by CRAN start R and then type 

.. code-block::

	install.packages("ggplot2")

Then you have to choose a mirror where to download from. Afterwards you can load a packages with

.. code-block::

	library("ggplot2")
	
This will be done automatically using UROPA. 
	
- `gplots`_
- `gridExtra`_ 
- `jsonlite`_ 
- `VennDiagram`_ 
- Vennerable
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