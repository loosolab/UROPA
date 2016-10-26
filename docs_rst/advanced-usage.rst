Advanced usage
==============

Combinations of query-specific keys
-----------------------------------

The keys provided in the config file are independent (with exception of
filter.attribute + attribute.value), so the combination of non-default
values for some of them can enhance and enrich the annotation results.

-  **feature.anchor + direction** : If 'feature.anchor': 'end' and the
   'direction': 'upstream', the centers of annotated peaks are located
   upstream of the feature and the distance to the end of the gene is
   smaller than the specified distance. If peaks upstream of the end
   position should be annotated, it might be better to not use the
   distance key with two values, like 'distance': [5000,0] and reject the
   direction key.

-  **feature.anchor + internals** : The feature.anchor will be used for
   measuring the closest distance to the peak center, only the features
   in this cut-off will be annotated. But if 'internals': True, also peaks
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