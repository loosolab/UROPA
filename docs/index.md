**Welcome to the UROPA documentation!**

UROPA is a peak annotation tool which can easily be fitted to your requirements.

**Overview**

UROPA is a tool for facilitatingthe analysis of next-generation sequencing methods for chromatin biology, like ChIP-seq or ATAC-seq. 
There are already different peak annotation tools, like HOMER or ChIPpeakAnno, but the advantage of UROPA is, that it is very easy to suit the annotation to your current analysis.
UROPA was developed as an open source analysis pipeline for peaks generated from any peak caller, e.g. MUSIC.

**Advantages of UROPA**

* Annotation with default values 
* Usage of all available gtf files as annotation database
* Detect the most appropriate annotation with flexible keys that allow robustness and simple customization, such as
	* feature type
	* feature position
	* feature direction relative to peak location
	* peak strand
	* internal features to large peaks
* Usage of custom annotation files
* One run with multiple sets of parameters by multiple queries
* Gives all annotations that fit to config file: Represented in the All_hits output
* Gives also the best annotation if more than one is identified: Represented in the Best_hits output
* Run with multiple sets of parameters at once by several queries
* Graduated annotation with the priority key              



**How to cite**

Please cite the paper describing UROPA when using it in your research:
tba

**Contribute**

Source Code: https://github.molgen.mpg.de/loosolab/UROPA     
Further details see [here](docs/install.md)

**Support**

If you have any issue feel free to send an email to Maria Kondili (maria.kondili@mpi-bn.mpg.de)

**Licence**

The project is licenced unter the MIT licence
