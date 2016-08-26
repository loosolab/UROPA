UROPA ('Universal RObust Peak Annotator') is a tool designed for annotating peaks generated from any peak caller (e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq), derived from next-generation sequencing methods for chromatin biology (e.g.  ChIPseq, ATACseq, FAIREseq). 

The annotation source is a GTF file, which provides the information of the genomic features to be used for annotation of the overlapping enriched regions (peaks). 
The annotation file as well as the peaks file should be defined in a configuration file, together with certain parameters that specify which features should be selected. 
The output is given in an easily-readable tab-delimited table with the corresponding annotation, as it is validated by the configuration file for each peak. 
Detailed information about the configuration file is in the section [Configuration file](http://uropa.readthedocs.io/en/latest/config/) and about the annotation output tables in the section [Output](http://uropa.readthedocs.io/en/latest/output/). 

Running UROPA is very simple. It can be executed in UNIX environment in one command line. 
By editing the configuration file all necessary parameters will be defined to obtain the peak annotation immediately. Within this configuration file, the peak bed file and the annotation GTF file need to be specified.
Without defining further parameters, the peaks will be annotated with a default annotation. To adjust the annotations to very fexible requirements, the different parameters of the config file should be used. 
Examples of application are presented in the [Usage Examples](http://uropa.readthedocs.io/en/latest/uropa-example/). Further exploration is suggested.

To start the UROPA peak annotation, the basic command has to look like this:

	uropa.sh –i <config.json> –o <Output_dir_name>

A template of the file config.json is provided by downloading UROPA. A quick overview about UROPA is displayed with uropa.sh -h, and instructions about the parameters with uropa.sh -u.

If one would like to have verbosity when running UROPA and obtain a file where all the steps of the annotation are explained in details for each peak, a –-verbose option is available, too:      

	uropa.sh –i config.json –o <Output_dir_name> –v <verbose_file.log>