UROPA ('Universal RObust Peak Annotator' ) is a tool designed for annotating peaks generated from any peak caller
(e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq), originating from any of the existing methods of 
accessible chromatin-based sequencing (e.g. ATACseq, ChIPseq, FAIREseq). 

The annotation source is a 'gtf' file, which provides the information of the genomic features to be used for annotation 
of the overlapping enriched regions (peaks). 
The annotation file as well as the peaks file should be defined in a configuration file, together with certain parameters that specify which features should be selected. 
The parameters will be explained more extensively later.
The output is given in an easily-readable tab-delimited matrix with the corresponding annotation,
as it is validated by the configuration file for each peak. 
Examples of the input configuration file and the output matrices will be shown in the following sections. 

Running UROPA is very simple. It can be executed in UNIX environment in one command line. 
By editing the configuration file you define all necessary parameters and you obtain the peak annotation immediately. 
The parameters are flexible and default values allow a simple annotation too. Examples of using them will be shown in the following sections.
Further exploration is strongly suggested.

The only required input arguments are the configuration file and the desired name of the output directory that will be created if not existent. 
So, one can launch UROPA by the command: 

	uropa.sh –i <config.json> –o <Output_dir_name*>

A template of the file ‘config.json’ is provided when you download UROPA and the instructions for completing it
are described in the section 'Configuration file'_configuration.rst. 
There is freedom in the use of parameters, as UROPA can also run with default options.
You can see these instructions in more details in the --help menu of UROPA in command line: 
	
	uropa.sh –h & uropa.sh –u    

If one would like to have verbosity when running UROPA and obtain a file where all the steps of the annotation are explained in details for each peak,
a –-verbose option is available, too:      

	uropa.sh –i config.json –o <Output_dir_name> –v <debug_file.log>

A template of the file ‘config.json’ is provided when you download UROPA. 
There is freedom in the use of parameters, as UROPA can also run with default options.
You can see these instructions in more details in the --help menu of UROPA in command line: 
uropa.sh –h & uropa.sh –u

