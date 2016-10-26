Installation
============
For developping UROPA the following versions were used (make sure all prerequisites are met):

* `R/Rscript <http://www.r-project.org/>`_ , v3.3.0
* `Python <http://continuum.io/downloads>`_, v2.7.8-anaconda-2.1.0

Required packages
-----------------

For Bash:
~~~~~~~~~
- `htslib 1.3.2 <http://www.htslib.org/download/>`_

For python:
~~~~~~~~~~~
- alumpy
- pysam


For R:
~~~~~
- `ggplot2 <https://cran.r-project.org/web/packages/ggplot2/index.html>`_
- `gplots <https://cran.r-project.org/web/packages/gplots/index.html>`_
- `gridExtra <https://cran.r-project.org/web/packages/gridExtra/index.html>`_
- `jsonlite <https://cran.r-project.org/web/packages/jsonlite/index.html>`_
- `VennDiagram <https://cran.r-project.org/web/packages/VennDiagram/index.html>`_
- Vennerable
- If multiprocessing should be used: `snow <https://cran.r-project.org/web/packages/snow/index.html>`_



**TODO** what else?

Install UROPA locally
---------------------

Run:

.. code:: bash

    git clone https://github.molgen.mpg.de/loosolab/UROPA.git
	export PATH=$PATH:dir/to/uropa/src

Now you can run uropa with the specified configuration file and the annotation database of interest. 
