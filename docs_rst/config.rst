Configuration file
==================
The configuration file is a **JavaScript Object Notation** formatted file that allows keys and
values easily to be set. For running UROPA, a template of
the config file as below is provided:

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

Three global keys are mandatory: ``'queries'``, ``'gtf'``, and ``'bed'``, additionally
there is an optional global key ``'priority'``.                
In a default annotation, only the ``'gtf'`` and ``'bed'`` keys needs to be specified by the user (relative file paths). The key ``'queries'`` has to be present in the config file, but can be left empty
(e.g. ``"queries": []``). Empty or missing key-value pairs are filled with their default values by UROPA.

Queries
-------

The ``'queries'`` key field is a list with 1 to n entries, each specifying  one valid annotation query with specific parameters
for UROPAs annotation process.

.. hint:: 

	-  	If more than one query is given, curly brackets should be used
		, for example ``[{}, {}]``.
	-  	Doublecheck spelling of keywords and comma settings, otherwise the
		UROPA annotation might differ from expectations.

Each query can specify the following keys:

.. rubric:: Query-specific keys

-  **feature**: Peaks will be annotated only to listed features from the 3rd column of the file specified by ``'gtf'``.
   
   Default: All available features from ``'gtf'``.
   
   Example: ``'feature': ['gene','transcript']`` or ``'feature': 'exon'``.

   
-  **feature.anchor**: The position(s) from which the distance
   to the peak center will be calculated. The best annotation is defined as the minimum distance if multiple anchors are defined. Valid distances are less or equal to the distance key value(specified by ``'distance'``, see below).            
   
   Default: ``['start', 'center', 'end']``
   
   Example: ``'feature.anchor': ['start']``

   
-  **distance**: Maximum permitted distance from the genomic feature anchor to the peak
   center. If only one value is given, this distance is valid in both directions from the
   feature anchor. If two values are given, the first value corresponds to the distance upstream of the feature
   anchor, and the second value to the distance downstream of the feature anchor.        
   
   Default: ``100000``
   
   Example: ``'distance': [2000,5000]`` or ``'distance': [5000]`` or ``'distance': 5000``.

   
-  **strand**: The desired strand of the annotated feature relative to the peak. 
   A constraint on strand specificity is only successfully evaluated if strand information is available for the feature **and** the peak.
   
   Default: ``['ignore', 'same', 'opposite']``
   
   Example: ``'strand': ['same']`` or ``'strand': 'same'``.

-  **direction**: Define the peak location relative to the feature's location, in respect of its orientation.
   A peak is 'upstream' if its center is upstream of a feature anchor position. Accordingly, a peak is 'downstream' if its center is downstream of a feature anchor position.
   Visual repesentation in :ref:`Figure 1 <genomic-location>` of section :doc:`/uropa-example` 
   
   Default: ``'any_direction'``
   
   Example: ``'direction': ['upstream','downstream']``
      
-  **internals**: This key represents a modifier with respect to the ``'distance'`` key. 
	This can be helpful to annotate peaks to features with a wide size range, such as genes, 
	which would otherwise be removed due to the distance thresholds. So even if the desired feature anchor is located too far away, 
	a feature can still be included if it is overlapped. Visual repesentation in :ref:`Figure 1 <genomic-location>` of section :doc:`/uropa-example`.

   ``'center'``: If the center of a peak intersects with a feature region or vice versa, the ``'distance'`` key filtering is disabled. This parameter ensures that the majority of the peak intersects with the feature.
   
   ``'any'``: If a peak intersects with a feature region or vice versa, the ``'distance'`` key filtering is disabled. An overlap of >= 1 nt is sufficient.
   
   ``'none'``: Internals key is turned off. The ``'distance'`` key is active.
   
   Allowed values are one of ``'none', 'center', 'any'.``
   
   Furthermore, ``'T', 'True', 'Y', 'Yes'`` are allowed and will be treated as ``'center'``,
   
   ``'F', 'False', 'N', 'No'`` are allowed and will be treated as ``'none'``.
   
   Default: ``'none'``
   
   Example: ``'internals':'center'``
   
   

-  **filter.attribute** : Key filters the attributes found in the 9th column of the GTF file.
   If a ``'filter.attribute'`` is given, only features that have a ``'attribute.value'`` for this attribute is kept as valid annotations. If this key is set, the key ``'attribute.value'`` is mandatory, too (see below).          
   
   Default: ``'None'``
   
   Example: ``'filter.attribute': ['gene_type']``

   
-  **attribute.value** : Corresponding attribute value for the ``'filter.attribute'`` found in the 9th column of the GTF file.
   If a ``'filter.attribute'`` is given, only features that have a ``'attribute.value'`` for this attribute can be valid annotations.
   
   Default: ``'None'``
   
   Example: ``'attribute.value': ['protein_coding']``

   
-  **show.attributes**: A list of attributes found in the 9th column of the GTF file which should appear in the final output tables. 
   If non existent attributes are specified, annotated peaks will display ``'NA'`` for those attributes. If set to ``'all'`` the list of attributes will be defined from all possible attributes in the annotated features from the gtf.
   
   Default: ``'None'``
   
   Example: ``'show.attributes':['gene_id', 'gene_biotype']``

Prioritizing queries
--------------------

**priority**: Allows multiple queries to be treated as a hierarchy, which means that a peak can be annotated according to subsequent queries only if no match to the preceding query is found. 
If 'False', all given queries are weighted equally and any feature matching with any of these queries will be a valid annotation.
If only one query is provided, the value of 'priority' has no influence on the annotation process.
Allowed values are one of ``'T', True', 'Y', 'Yes'`` or ``'F', 'False' ,'N' ,'No'``.

Default: ``'False'``

Example: ``'priority':'Yes'``

Annotation database (GTF)
-------------------------

**gtf**: A path to a file in standard GTF format (9 columns), as described by `Ensembl GTF format`_.
The GTF file acts as annotation database. If your annotation database is not in the Ensembl GTF format, a conversion can be done by
UROPA. For more information see :doc:`/custom`.

**Required**, no default.

Genomic regions (BED)
---------------------

**bed**: A path to a file in BED format, as described by `Ensembl Bed format`_. 
The BED file can be any tab-delimited file containing the genomic regions, e.g. enriched regions from a peak-calling tool (e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq), with a minimum of 3 columns (chr/start/stop).

**Required**, no default.

.. _Ensembl GTF format: http://www.ensembl.org/info/website/upload/gff.html
.. _Ensembl Bed format: http://www.ensembl.org/info/website/upload/BED.html

.. role:: bash(code)
   :language: bash
