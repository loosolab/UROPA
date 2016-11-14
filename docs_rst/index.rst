Welcome to the UROPA documentation!
===================================
UROPA is a command line based tool intended for genomic region
annotation. 


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
-  Multiple output tables (AllHits, FinalHits, BestperQuery\_Hits)
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files with the UROPA to GTF utility

**How to cite**

Please cite the paper describing UROPA when using it in your research: *tba*

**PDF version**

Choose master version for better pdf layout. 

.. hint::
  - On the bottom right there is a drop down menu
  - click latest
  - click PDF

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
   output-pdf
   uropa-example
   custom
   license
   help
   