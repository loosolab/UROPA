Configuration file
==================
The configuration file is a **JavaScript Object Notation** formatted file that allows keys and
values to be put in easily as textform. For running UROPA, a template of
the config file as below will be provided:

.. code:: json

    {
    "queries":[ 
        {"feature":"",    "feature.anchor": "",    "distance":"",    "strand":"",
		"direction":"",    "internals":"",     "filter.attribute":"",    
		"attribute.value":"",     "show.attributes":"" }
              ],
    "priority": "",
    "gtf": ".gtf",
    "bed": ".bed"
    }

Three keys are required: ``'queries'``, ``'gtf'``, and ``'bed'``, additionally
there is an optional key ``'priority'``.                
In a default annotation, only the ``'gtf'`` and ``'bed'`` keys are specified with file paths. The queries key has to be present in the config file, but can be left empty
(``'queries": []``,). Empty or missing key-value pairs are filled with their default values by UROPA.

Queries
-------

The queries key field is a list with (potentially) many queries, each specifying query-specific parameters
for UROPAs annotation process.

.. hint:: 

	-  	If more than one query is given, they should be included in curly brackets
		like all values, i.e ``[{}, {}]``.
	-  	Make sure of correct spelling and comma placement, otherwise the
		UROPA annotation can be different as expected.

Each query can specify the following keys:

Query-specific keys
~~~~~~~~~~~~~~~~~~~

-  **features**: Peaks will be annotated only to listed features from the 3rd column of the file specified by ``'gtf'``.
   
   Default: All features from ``'gtf'``.
   
   Example: ``'features': ['gene','transcript']`` or ``'feature': 'exon'``.

-  **feature.anchor**: The position(s) from which the distance
   to the peak center will be calculated. The best annotation conforms to
   the closest distance if it is less or equal to the maximum permitted distance (specified by ``'distance'``, see below).            
   
   Default: ``['start', 'center', 'end']``
   
   Example: ``'feature.anchor': ['start']``

-  **distance**: Maximum permitted distance from the genomic feature anchor to peak
   center. If one value is gievn, this distance is allowed in both directions from the
   feature anchor. If two values are given, the first value corresponts to the maximum permitted distance upstream of the feature
   anchor, and the second value to the maximum permitted distance downstream of the feature anchor.        
   
   Default: ``100000``
   
   Example: ``'distance': [2000,5000]`` or ``'distance': [5000]`` or ``'distance': 5000``.

-  **strand**: The desired strand of the annotated feature relatve to the peak. Can be 'same', for feature and peak residing on the same strand, 'opposite' or 'both'. 
   A contraint on strand specificity is only successful evaluated if strand information is available for the feature and the peak.
   
   Default: ``['same', 'both', 'opposite']``
   
   Example: ``'strand': ['same']`` or ``'strand': 'same'``.

-  **direction**: Defining the peak location relative to the feature's location inclusive its orientation.
   A peak is 'upstream' if its center is upstream of a feature anchor position. Similarly, a peak is 'downstream' if its center is downstream of a feature anchor position.
   Also compare to Figure 2 in :doc:`/uropa-example`.
   
   Default: ``'any\_direction'``
   
   Example: ``'direction': ['upstream','downstream']``

-  **internals**: Allowing 'internals' will render valid annotation possible if a feature is found inside a peak region or vice versa.
   This works even if the distance to the 'feature.anchor' is larger than the maximum permitted 'distance'. 
   This key can be helpful to identify peaks all along the feature or for the allocation of ATAC-seq peaks to very small transcription factor binding sites.
   Allowed values are one of ``'T', True', 'Y', 'Yes'`` or ``'F', 'False' ,'N' ,'No'``.
   
   Default: ``'False'``
   
   Example: ``'T'``

-  **filter.attribute** : One of the attribute keys found in the 9th column of the GTF file.
   If a ``'filter.attribute'`` is given, only features that have a ``'attribute.value'`` for this attribute can be valid annotations. This key is needed to cooccur with the key ``'attribute.value'`` (see below).          
   
   Default: ``'None'``
   
   Example: ``'filter.attribute': ['gene_type']``

-  **attribute.value** : Corresponding attribute value for the ``'filter.attribute'`` found in the 9th column of the GTF file.
   If a ``'filter.attribute'`` is given, only features that have a ``'attribute.value'`` for this attribute can be valid annotations.
   
   Default: ``'None'``
   
   Example: ``'attribute.value': ['protein\_coding']``

-  **show.attributes**: A list of attributes found in the 9th column of the GTF file which should appear in the output tables. 
   If nonexistent attributes are specified, annotated peaks will display ``'not.found'`` in for those attributes.                  
   
   Default: ``'None'``
   
   Example: ``['gene\_id', 'gene\_biotype']``

Prioritizing queries
--------------------

**priority**: Allows multiple queries to be treated as a hierarchy, which means that a peak can be annotated according to subsequent queries only if no match to the preceding query is found. 
If 'False', all given queries are weighted equally and any feature matching with any of these queries will be a valid annotation.
If only one query is provided, the value of 'priority' has no influence on the annotation process.
Allowed values are one of ``'T', True', 'Y', 'Yes'`` or ``'F', 'False' ,'N' ,'No'``.

Default: ``'False'``

Example: ``'Yes'``

GTF annotation database
-----------------------

**gtf (required)**: A path to a file in standard GTF format (9 columns), as described by `Ensembl GTF format`_.
The GTF file acts as annotation database. If your annotation database is not in the Ensembl GTF format, a conversion can be done by
UROPA. For more information see :doc:`/custom`.


Genomic regions (BED)
---------------------

**bed (required)**: A path to a file in BED format, as described by `Ensembl Bed format`_. 
The BED file can be any tab-delimited file containing the genomic regions, e.g. enriched regions from a peak-calling tool (e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq), with a minimum of 3 columns.

.. _Ensembl GTF format: http://www.ensembl.org/info/website/upload/gff.html
.. _Ensembl Bed format: http://www.ensembl.org/info/website/upload/BED.html

.. role:: bash(code)
   :language: bash
