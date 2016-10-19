If you have trouble please email maria.kondili@mpi-bn.mpg.de

FAQ
===
Here some frequently asked questions are answered:

* **How to define multiple queries in the configuration file?**
	"queries":[{},{}]
	the total of all queries should be in squared brackets and a single query inside culy brackets. Different queries are sepreated by commas. 
* **What is the tabix Error about?**
	This error occurs if not all genomic locations represented in the peak file, are also constituted in the GTF annotation file. 
	Those peaks can not be annotated and will be NA in the outputs.
* **How to annotate with default values?**
	In order for the default values to be active, the key itself shouldn't be present and empty in the config file. So if only some keys should be default, leave them out.
	If you want to annotate with only default values, do not remove the queries key, but leave it empty like "queries":[] **ATTENTION** annotated peaks will be displayed without any assignment, so you do not know what for the peaks are annotated!
* **Where are multiple best hits in FinalHits?**
	If there are multiple annotations with the same distance representing the best annotation (minimal distance), only the first will be represented in the FinalHits. If an overview about all is requested, the AllHits can be used. 

	
Got any other questions? Contact maria.kondili@mpi-bn.mpg.de
