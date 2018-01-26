Welcome to the UROPA documentation!
===================================

.. image:: https://img.shields.io/badge/Install%20with-conda-green.svg?style=plastic&logoWidth=40
    :target: https://conda.anaconda.org/bioconda
.. image:: https://badge.fury.io/py/uropa.png
    :target: https://badge.fury.io/py/uropa

UROPA is a command line based tool intended for genomic region annotation.


**Advantages of UROPA**

-  Detect the most appropriate annotation of peaks, utilizing parameters such as

   -  feature type
   -  feature anchor
   -  feature direction relative to peak location
   -  filtering for attribute values, e.g. “protein\_coding”
   -  strand specificity

-  Utilization of any available GTF files as annotation reference
-  Multiple queries can be processed in a single run
-  Graduated annotation due to prioritization
-  Multiple output tables (allhits, finalhits, besthits)
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files with the UROPA to GTF utility

**How to cite**

Please cite the paper describing UROPA when using it in your research: **Kondili M, Fust A, Preussner J, Kuenne C, Braun T, Looso M. UROPA: a tool for Universal RObust Peak Annotation. Scientific Reports. 2017;7:2593. doi:10.1038/s41598-017-02464-y.**

**Contribute**

- `Issue Tracker`_
- `Source Code`_

.. _Issue Tracker: https://github.molgen.mpg.de/loosolab/UROPA/issues
.. _Source Code: https://github.molgen.mpg.de/loosolab/UROPA


**Support**

If you have any issue feel free to send an email to `Mario Looso <mario.looso@mpi-bn.mpg.de>`_

**Licence**

The project is licensed under the MIT license (see :doc:`/license`)

.. toctree::
   :maxdepth: 3
   :caption: Content of this manual

   introduction
   install
   parameter
   config
   output
   uropa-example
   custom
   uropa_gui
   license
   help
