Usage
======

Command-line parameters
--------------------

List of current parameters for command-line usage and their explanation:

.. code:: bash

	
	Usage: uropa [options]
	
	UROPA - Universal RObust Peak Annotator.

	optional arguments:
	  -h, --help                       show this help message and exit

	Arguments for one query:
	  -b , --bed                       Filename of .bed-file to annotate
	  -g , --gtf                       Filename of .gtf-file with features
	  --feature [ [ ...]]              Feature for annotation
	  --feature-anchor [ [ ...]]       Specific feature anchor to annotate to
	  --distance [ [ ...]]             Maximum permitted distance from feature (1 or 2
					   arguments)
	  --strand                         Desired strand of annotated feature relative to peak
	  --relative-location [ [ ...]]    Peak location relative to feature location
	  --internals                      Set minimum overlap fraction for internal feature
					   annotations. 0 equates to internals=False and 1 equates
					   to internals=True. Default is False.
	  --filter-attribute               Filter on 9th column of GTF
	  --attribute-values [ [ ...]]     Value(s) of attribute corresponding to --filter-
					   attribute
	  --show-attributes [ [ ...]]      A list of attributes to show in output (default: all)

	Multi-query configuration file:
	  -i config.json, --input config.json
					   Filename of configuration file (keys in this file
					   overwrite command-line arguments about query)

	Additional arguments:
	  -p , --prefix                    Prefix for result file names (defaults to basename of
					   .bed-file)
	  -o , --outdir                    Output directory for output files (default: current
					   dir)
	  --output-by-query                Additionally create output files for each named query
					   seperately
	  -s, --summary                    Create additional visualisation of results in graphical
					   format
	  -t n, --threads n                Multiprocessed run: n = number of threads to run
					   annotation process
	  -l uropa.log, --log uropa.log    Log file name for messages and warnings (default: log
					   is written to stdout)
	  -d, --debug                      Print verbose messages (for debugging)
	  -v, --version                    Prints the version and exits
	  -c , --chunk                     Number of lines per chunk for multiprocessing (default:
					   1000)



		
.. note::
	The ``-p`` parameter can either contain the prefix of the result files, like ``-p abc`` gives abc_allhits.txt in the working directory,
	or the result directory and prefix, like ``-p xy/abc`` which stores the result files in directory xy. If the directory xy is not existing, it will be created.
	
Docker container usage
---------------------

.. code:: bash	

	sudo docker run --rm -v <path-to-input-files-on-HOST>:<path-to-container-mnt> UROPA:LATEST uropa <UROPA-Paramters> -p <path-to-container-mnt>/'your-file-prefix'
	

.. note::

	``-v`` parameter mounts a HOST folder into your docker CONTAINER. This folder should contain the input files for UROPA and also the result files will be stored here. 
	No files will be stored in the container!!
	``--rm`` removes/closes the container after the run
	Make sure to use the uropa -p option specifying the output directory and prefix, otherwise results are lost in the container environment!
	
