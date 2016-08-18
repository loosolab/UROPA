**Welcome to the UROPA documentation!**

UROPA is a peak annotation tool which can easily be fitted to your requirements.
Download UROPA: tba

**Overview**

There are already different peak annotation tools, like HOMER or ChIPpeakAnno,
but with none of them it is so easy to suit the annotation to your currant analysis. 
UROPA was developed as an open source analysis pipeline for peaks generated from any 
peak caller, e.g. MUSIC, originating from any of the existing methods of accessible
chromatin-based sequencing, as ChIP-seq or ATAC-seq.

**Advantages of UROPA**

* Annotation with default values 
* Usage of all available gtf files as annotation database
* Detect the most appropriate annotation with flexible keys that allow robustness and simple customization, such as
	* feature type
	* feature position
	* feature direction relative to peak location
	* peak strand
	* internal features to large peaks
* One run with multiple sets of parameters by multiple queries
* Gives all annotations that fit to config file: Represented in the All_hits output
* Gives also the best annotation if more than one is identified: Represented in the Best_hits output

* Run with multiple sets of parameters at once by several queries
* Graduated annotation with the priority key
* Usage of custom annotation files
**How to cite**

Please cite the paper describing UROPA when using it in your research:
tba

**Contribute**

Source Code: https://github.molgen.mpg.de/loosolab/UROPA

**Support**

If you have any issue feel free to send an email to Maria Kondili (maria.kondili@mpi-bn.mpg.de)

**Licence**

The project is licenced unter the MIT licence
