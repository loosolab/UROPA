Configuration file
==================
The configuration file is a .json format file that allows keys and
values to be input easily and clearly. For running UROPA, a template of
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

There are three required keys: 'queries', 'gtf', and 'bed', additionally
there is an optional keys: 'priority'.                
In a default annotation, only the GTF and BED keys are specified. The queries key has to be present in the config file, but can be left empty
("queries":[],). All default key values are used.

queries
-------

The very important queries key field with nested keys specifies the
UROPA annotation process. It can contain more than one query, written
inside '{}' and separated with commas.

.. hint:: 

	-  	If more than one query is given, they should be included in brackets
		like all values, i.e [{}, {}].
	-  	Make sure of correct spelling and comma placement, otherwise the
		UROPA annotation can be different as expected.

It accepts the following keys for each query:

keys
~~~~

-  **features** :['gene','transcript'] Or whatever features are defined
   in the 3rd column of the 'GTF'.       
   By default all features present in the 'GTF' will be used.

-  **feature.anchor** : ['start'] The position from which the distance
   to the peak center will be analyzed. The best annotation conforms to
   the closest distance. If default values are used, the distance from the peak center to all positions of the feature will be analyzed
   and if the minimum of the three calculated distances is less or equal to the specified distance key, the feature
   will be accepted for annotation.              
   **Default: ['start', 'center', 'end']**.

-  **distance**: [2000] or [5000,1000] Maximum allowed distance from the genomic feature anchor to peak
   center. If only one distance is specified, this distance is allowed in both directions from the
   feature anchor. If there are two distances defined, the first distance correspont to the distance upstream of the feature
   anchor, and the second distance to the distance downstream of the feature anchor.          
   **Default: 100000**.

-  **strand**: ['same'] The strand on which the annotated feature should
   be. If this feature should be specified, make sure that strand information is prepared.         
   **Default: ['same', 'both', 'opposite']**. 

-  **direction** : ['upstream','downstream'] Defining the peak
   location relative to the feature's location inclusive its orientation.
   A peak is 'upstream' when its center is upstream of a feature start
   position. Similar for downstream but to the end position of a
   feature (compare Figure 2 in :doc:`/uropa-example`). If this key is
   specified, only peak located upstream/overlapStart or rather
   downstream/overlapEnd will be annotated.     
   **Default:'any\_direction'**.

-  **internals**: ['T',True','F','False','Y','Yes','N','No'] If True,
   the features found inside a peak region OR a peak found inside a
   feature region will be considered as valid for annotation, even if
   the distance to the 'feature.anchor' is further than the desired
   'distance'. This key can be helpful to identify peaks all along the
   features, or for the allocation of ATAC-seq peaks to very small
   transcription factor binding sites(tfbs).        
   **Default:'False'**.

-  **filter.attribute** : ['gene\_type'] Attribute key found in the 9th
   column of the GTF file for which should be filtered. This key is linked to the 'attribute.value'.          
   **Default:'None'**.

-  **attribute.value** : ['protein\_coding'] Corresponding attribute value found in the 9th
   column of the GTF file for which should be filtered. If the two linked keys are specified, only features accomplishing the specification of those keys will be used for annotation.       
   **Default:'None'**.

-  **show.attributes**: ['gene\_id', 'gene\_biotype'] Attributes found in the 9th
   column of the GTF file which should be displayed in the output tables. The minimum overlap of all 'show.attributes' across as queries will be displayed. 
   Thus, it is enough to specify them in the first query.
   If nonexistent attributes are specified, annotated peaks will display 'not.found' in
   this column.                  
   **Default: 'None'**.
   
Combination of config keys
~~~~~~~~~~~~~~~~~~~~~~~~~~

The keys provided in the config file are independent (with exception of
filter.attribute + attribute.value), so the combination of non-default
values for some of them can enhance and enrich the annotation results.

-  **feature.anchor + direction** : If feature.anchor:end and the
   direction:upstream the centers of annotated peaks are located
   upstream of the feature and the distance to the end of the gene is
   smaller than the specified distance. If peaks upstream of the end
   position should be annotated, it might be better to not use the
   distance key with two values, like distance:[5000,0] and reject the
   direction key.

-  **feature.anchor + internals** : The feature.anchor will be used for
   measuring the closest distance to the peak center, only the features
   in this cut-off will be annotated. But if internals:True, also peaks
   inside features and features inside peaks will be annotated, even
   with a distance larger than specified. The reported distance is still
   the one to the specified feature.anchor.

-  **direction + internals** : If 'direction' is given for filtering and
   'internals':'True', the features with 'upstream'/'downstream' peaks
   will be annotated, plus features inside peaks and peaks inside
   features. Upstream/downstream annotations have to be within the
   specified distance.

-  **filter.attribute + attribute.value** : The features for annotation
   will be filtered for the given 'attribute' key and only if they agree
   with the 'attribute.value' given, will they be associated to the
   peak. Both these values should be given to the config for the
   filtering to be successful.

-  **filter.attribute + show.attributes** : If the 'filter.attribute' is
   given, it is advised to also use the same key among others, at the
   'show.attributes' so that filtered results are verified. To be noted
   that 'show.attributes' can accept more than one attributes for
   displaying at the output tables.

.. note: The combination is affecting results accordingly, when given in the same query. If used in different queries, they work independently,they are not considered as combined.

priority
--------

**priority** : ['T', 'True', 'F', 'False', 'Y', 'Yes', 'N', or 'No']
This key is useful when more than one query is defined. If 'True', a peak can be annotated according to the second query, only if a feature matching to the first query is not found. Respectively for
further queries. If 'False', all given queries are considered equally and any feature matching with any of these queries will annotate the peaks. The query that allowed each feature to be selected for annotation will be shown 
in the last column of the output tables. If only one query is provided, the value of 'priority' can be 'True' or 'False', without any difference in the output annotation.        
**Default :'False'**. 

gtf
---

The GTF file should be of the standard GTF format (9 columns), as descriBED by `Ensembl GTF format`_ 
The GTF file acts as annotation database. If your annotation database is not in the right format, a conversion can be done by
UROPA. For more information see :doc:`/custom`.

bed
---

The BED file can be any tab-delimited file containing the detected enriched regions from a peak-calling tool (e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq) 
or any other table with genomic regions of a minimum of 3 columns and complying with the known BED format, as descriBED by `Ensembl Bed format`_.


.. hint: 

	In order for the default values to be active, the key itself shouldn't be present and empty in the config file. 
	In case there exist a key without value, an error message will advise you to fill in or omit the key.

.. _Ensembl GTF format: http://www.ensembl.org/info/website/upload/gff.html%3E
.. _Ensembl Bed format: http://www.ensembl.org/info/website/upload/BED.html
