Welcome to the UROPA documentation!
===================================
UROPA is a command line based tool intended for genomic region
annotation. Different target features can be prioritized with multiple integrated queries based on a configuration file.
Queries are sensitive for feature type, distance, strand specificity, feature attributes (e.g.
“protein\_coding”) or the anchor position relative to the feature. UROPA
can incorporate reference annotation files (GTF) from different sources,
like Gencode, Ensembl, or RefSeq, as well as custom reference files
produced by the user.


**Advantages of UROPA**

-  Detect the most appropriate annotation according to flexible parameters that allow
   robustness and simple customization of
   
   -  feature type,
   -  feature anchor,
   -  feature direction relative to peak location,
   -  filtering for attribute values, e.g. “protein\_coding”,
   -  strand specificity

-  Utilization of many available GTF files as annotation database
-  Multiple queries of variable parameter sets can be processed in a single run
-  Graduated annotation due to priorization
-  Different easily-readable output tables (AllHits, FinalHits, BestperQuery\_Hits)
-  Visual summary for annotation evaluation
-  Preparation of custom annotation files with the UROPA to GTF utility

**How to cite**

Please cite the paper describing UROPA when using it in your research: *tba*

**Contribute**

- `Issue Tracker`_
- `Source Code`_ 

.. _Issue Tracker: https://github.molgen.mpg.de/loosolab/UROPA/issues
.. _Source Code: https://github.molgen.mpg.de/loosolab/UROPA


**Support**

If you have any issue feel free to send an email to `Maria Kondili <maria.kondili@mpi-bn.mpg.de>`_

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
   license
   help
   