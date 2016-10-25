Application examples
====================
In this section several examples for the usage of the config file are presented. 
A detailed introduction of how to use the config file can be found in the section `Configuration file`_.
There is also a detailed information about the different output formats in the section `Output tables`_.

Example 1: 'feature.anchor' key
-------------------------------
UROPA allows a flexibility of annotation for features. With the key 'feature.anchor' it is possible to decide from where the distance to the peak should be calculated. 
Typically, the distance is calculated from the TSS, correspond to 'start' in UROPA. Furthermore, it is possible to use the 'center' and 'end' of the feature for the distance calculation. 

If no value is given, the distances from all three positions to the peak center are calculated and the closest is choosen. Only if the choosen distance is smaller or equal to the distance defined in the 'distance' key, the peak will be annotated for that feature.                                                                                        The position closer to the peak.center will be indicated in the output file in the column **'feat_anchor'**.

There are two queries with different 'feature.anchor' for this example. 

.. code:: json

    {"queries": [ 
        {"feature":"gene", "distance":5000, "feature.anchor": "start", "show.attributes":"gene_name"},       
        {"feature": "gene","distance":5000, "feature.anchor": "center"}],
    "priority" : "False",
    "gtf": "gencode.v19.annotation.gtf",
    "bed": "ENCFF001SUE.bed"}


