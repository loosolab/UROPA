Parameters
==========
List of current parameters for command-line usage and their explanation:

.. code:: bash

        Usage: uropa.py [options]

        Available options:

        -h, --help             	print this help message and further details on the configuration file
        -i, --input            	filename of configuration file [mandatory]
        -p, --prefix           	prefix for output file, can include subdirectories [basename of --input]
        -r, --reformat         	create an additional compact and line-reduced table as result file
        -s, --summary          	additional visualisation of results in graphical format will be created
        -t n, --threads n      	multiprocessed run: n = number of threads to run annotation process
        -add-comments          	show comment lines in output files explaining the columns
        -l, --log              	log file name for messages and warnings
        -d, --debug            	print verbose messages (for debugging purposes)
        -v, --version          	print the version and exit
