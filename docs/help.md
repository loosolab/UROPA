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

Got any other questions? Contact maria.kondili@mpi-bn.mpg.de
