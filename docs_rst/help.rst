Help
====
If you have trouble please email `Mario Looso <mario.looso@mpi-bn.mpg.de>`_.                                    
Please report bugs on our Github `issue tracker <https://github.molgen.mpg.de/loosolab/UROPA/issues>`_.
They will be addressed as soon as possible. 

**FAQ**


* **How to define multiple queries in the configuration file?**
	"queries":[{},{}]
	the total of all queries should be in squared brackets and a single query inside curly brackets. Different queries are separated by commas. 
* **What is the tabix Error about?**
	This error occurs if not all genomic locations represented in the peak file, are also constituted in the GTF annotation file. 
	Those peaks can not be annotated and will be NA in the outputs.
* **How to annotate with default values?**
	In order to activate default values, the key itself shouldn't be present in the config file. 
	If you want to annotate with default values only, do not remove the queries key, but leave it empty like "queries":[] 


