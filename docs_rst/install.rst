Installation
============
For developping UROPA the following versions were used (make sure all prerequisites are met):

- `R/Rscript`_, v3.3.0
- `Python`_ , v2.7.8-anaconda-2.1.0

Required packages
-----------------

For Bash:
~~~~~~~~~
- `htslib`_ 1.3.2

For python:
~~~~~~~~~~~
- alumpy
- pysam


For R:
~~~~~
- `ggplot2`_
- `gplots`_
- `gridExtra`_ 
- `jsonlite`_ 
- `VennDiagram`_ 
- Vennerable
- If multiprocessing should be used: `snow`_ 

**TODO** what else?

Install UROPA locally
---------------------

Run:

.. code:: bash
   git clone https://github.molgen.mpg.de/loosolab/UROPA.git
   export PATH=$PATH:dir/to/uropa/src

Now you can run uropa with the specified configuration file and the annotation database of interest. 

.. _R/Rscript : http://www.r-project.org/
.. _Python: http://continuum.io/downloads
.. _htslib: http://www.htslib.org/download/
.. _ggplot2: https://cran.r-project.org/web/packages/ggplot2/index.html
.. _gplots: https://cran.r-project.org/web/packages/gplots/index.html
.. _gridExtra: https://cran.r-project.org/web/packages/gridExtra/index.html
.. _jsonlite: https://cran.r-project.org/web/packages/jsonlite/index.html
.. _VennDiagram: https://cran.r-project.org/web/packages/VennDiagram/index.html
.. _snow: https://cran.r-project.org/web/packages/snow/index.html