Welcome to the UROPA documentation!
===================================

UROPA is a command line based tool, intended for genomic region
annotation. Based on a configuration file, different target features can
be prioritized with multiple integrated queries. These can be sensitive
for feature type, distance, strand specificity, feature attributes (eg.
protein_coding) or the anchor position relative to the feature. UROPA
can incorporate reference annotation files (GTF) from different sources,
like Gencode, Ensembl, or RefSeq, as well as custom reference files
produced by the user.

Advantages of UROPA
-------------------

-  Simple usage: No programming
-  Utilization of all available GTF files as annotation database
-  Detect the most appropriate annotation with flexible keys that allow
   robustness and simple customization, such as

   -  feature type
   -  feature anchor
   -  feature direction relative to peak location
   -  filter for attribute values, e.g. “protein\_coding”
   -  strand specificity

-  Preparation of custom annotation files
-  One run with multiple sets of parameters by multiple queries
-  Graduated annotation due to priorization
-  Different easily-readable output tables (AllHits, FinalHits,
   BestperQuery\_Hits).
-  Visual summary for annotation evaluation
-  Annotation with default values

How to cite
------------

Please cite the paper describing UROPA when using it in your research:
tba

Contribute
----------

Source Code see <https://github.molgen.mpg.de/loosolab/UROPA)/>
Further details see <http://uropa.readthedocs.io/en/latest/install/>

Support
-------

If you have any issue feel free to send an email to Maria Kondili
(maria.kondili@mpi-bn.mpg.de)

Licence
--------

The project is licensed under the MIT license

Contents:
----------

.. toctree::
   :maxdepth: 3

   introduction
   install
   parameter
   config
   output
   uropa-example
   custom
   license
   help
 