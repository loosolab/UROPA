UROPA ('Universal RObust Peak Annotator') is a tool facilitating the analysis of next-generation sequencing methods for chromatin biology, like ChIPseq or ATACseq. 
It is designed to annotate enrichted genomic regions (peaks) of interest generated from any peak caller (e.g. MACS2, MUSIC, FindPeaks, CisGenome, PeakSeq). 

The annotation source is a GTF file, which provides the information of the genomic features to be used for annotation of the peaks. The peaks should be represented in BED file format.
Annotation and peak files should be specified in the configuration file. Furthermore, certain parameters that define how peaks should be annotated can be adjusted. More [details](http://uropa.readthedocs.io/en/latest/config/). 
The output is given in easily-readable tab-delimited tables with the corresponding annotation, as it is validated by the configuration file for each peak. More [details](http://uropa.readthedocs.io/en/latest/output/). 

Running UROPA is very simple. It can be executed in UNIX environment in one command line. 
By editing the configuration file all necessary parameters will be defined to obtain the peak annotation immediately. Within this configuration file, the peak-bed file and the annotation-GTF file need to be specified,as well.
Without defining further parameters, the peaks will be annotated with a default annotation. To adjust the annotations to more flexible requirements, the different parameters of the config file should be used. 
Examples of application are presented in the [Usage Examples](http://uropa.readthedocs.io/en/latest/uropa-example/). Further exploration is suggested.

To start the UROPA peak annotation, the basic command should be :  

```bash
uropa –i <config.json> –o <output_dir>
```

A template of the file config.json is loaded in the working directory when downloading UROPA, named "a_config_example.json". A quick overview about UROPA usage is displayed with  *uropa -h*. 

