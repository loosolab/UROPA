Parameters
==========
List of current parameters for command-line usage and their explanation:

.. code:: bash

	Usage: uropa.py [options]

	Available options:

	-h, --help						print this help message and further details on the configuration file
	-i confing.json, --input confing.json	filename of configuration file [mandatory]
	-p prefix, --prefix	prefix		prefix for result files, can include subdirectories [basename of config]
	-r, --reformat					create an additional compact and line-reduced table as result file
	-s, --summary					additional visualisation of results in graphical format will be created
	-t n, --threads n				multiprocessed run: n = number of threads to run annotation process
	-add-comments					show comment lines in output files explaining the columns
	-l uropa.log, --log	uropa.log	log file name for messages and warnings
	-d, --debug						print verbose messages (for debugging purposes)
	-v, --version					print the version and exit

		
.. note::
	The ``-p`` parameter can either contain the prefix of the result files, like ``-p abc`` gives abc_allhits.txt in the working directory,
	
	or the result directory and prefix, like ``-p xy/abc`` which stores the result files in directory xy. If the directory xy is not existing, it will be created.