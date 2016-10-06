**Welcome to the UROPA documentation!**

UROPA is a peak annotation tool facilitating the analysis of next-generation sequencing methods for chromatin biology, like ChIPseq or ATACseq. 
There are already different peak annotation tools, like HOMER or ChIPpeakAnno, but the advantage of UROPA is, that it can easily be fitted to your requirements.
UROPA was developed as an open source analysis pipeline for peaks generated from any peak caller, e.g. MUSIC.

**Advantages of UROPA**

* Annotation with default values 
* Usage of all available GTF files as annotation database
* Detect the most appropriate annotation with flexible keys that allow robustness and simple customization, such as
	* feature type
	* feature position
	* feature direction relative to peak location
	* peak strand
* Preparation of custom annotation files
* One run with multiple sets of parameters by multiple queries
* Gives all annotations that fit to the custom configuration: Represented in the All_hits output
* Offers also the best annotation for each query, if more than one was identified: Represented in the Best_hits output
* For multiple queries the best annotation of all possible annotations across all queries is also provided: Merged_best_hits output
* Graduated annotation with the priority key
* Easily-readable output tables with rich information about exact distance and location of annotated features.
* Visual summary for annotation evaluation

**How to cite**

Please cite the paper describing UROPA when using it in your research:
tba

**Contribute**

Source Code: https://github.molgen.mpg.de/loosolab/UROPA     
Further details see [here](http://uropa.readthedocs.io/en/latest/install/)

**Support**

If you have any issue feel free to send an email to Maria Kondili (maria.kondili@mpi-bn.mpg.de)

**Licence**

The project is licensed under the MIT license
