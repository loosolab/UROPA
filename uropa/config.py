#!/usr/bin/env python
"""Contains functions for UROPA configuration."""
import json
import ast
import os
import subprocess
from textwrap import dedent
import numpy as np


def howtoconfig():
    """Defines the epilog that is given when help is requested."""
    epilog = dedent("""\
	UROPA is a peak annotation tool facilitating the analysis of next-generation sequencing methods for
	chromatin biology, like ChIPseq or ATACseq. There are already different peak annotation tools, like
	HOMER or ChIPpeakAnno, but the advantage of UROPA is, that it can easily be fitted to your requirements.
	UROPA was developed as an open source analysis pipeline for peaks generated from any peak caller.

	All parameters and paths to input or output files should be reported in a JSON configuration file.
	The configuration file should at least contain paths for bed and GTF files:

	{
	"queries": [],
	"bed": "/path/to/bed/file.bed",
	"gtf": "/path/to/annotation/file.gtf"
	}

	Different query types can be defined using the queries key:

	{
	"queries": [
	  {...},
	  {...}],
	"bed": "/path/to/bed/file.bed",
	"gtf": "/path/to/annotation/file.gtf"
	}

	Optionally, the priority key can be used to fine tune UROPAs behaviour:

	{
	"queries": [
	  {...},
	  {...}],
	"bed": "/path/to/bed/file.bed",
	"gtf": "/path/to/annotation/file.gtf",
	"priority": "True"
	}

	Please visit http://uropa-manual.readthedocs.io/config.html for detailed information on configuration.
	""")
    return epilog


def parse_json(infile):
    """Read a json file"""
    assert isinstance(infile, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format(
        'column', type(infile), 'str')

    with open(infile, 'r') as f:
        return ast.literal_eval(json.dumps(json.load(f)))


def column_from_file(file, column, log=None):
    """Extracts a given column from a file, and returns unified values as list."""
    assert isinstance(file, str), 'Argument {0} of wrong type ({1}), should be {2}!'.format(
        'column', type(file), 'str')
    assert isinstance(column, int), 'Argument {0} of wrong type ({1}), should be {2}!'.format(
        'column', type(column), 'int')

    cmd = 'cut -f' + str(column) + ' ' + str(file) + \
        ' | sort | uniq | grep -v "^#"'
    try:
        vals = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        if log is not None:
            log.warning("File {} might be empty or has not enough columns".format(file))
        return([])
    return([v for v in vals.split('\n') if v != ""])


def parse_parameters(config, log=None):
    """Fills the configuration with default values. Writes a warning to logs, if unknown keys are detected."""
    defaults = {"priority": "False", "bed": "no_peaks.bed",
                "gtf": "no_annotation.gtf"}  # , "bigwig": "none.bw"
    keys = defaults.keys()
    values = map(lambda x: config[x] if x in config else defaults[x], keys)

    if log is not None:
        unknown = [k for k in config.keys() if k not in keys and k !=
                   "queries"]
        if any(unknown):
            log.warning(
                "Unknown keys detected in configuration: {}".format(unknown))
    parameters = dict(zip(keys, values))
    return parameters


def parse_queries(config, gtf_feat, log=None):
    """Adds in defaults where query parameters are missing."""
    defaults = {"feature": gtf_feat, "strand": "ignore", "show.attributes": "None", "filter.attribute": "None",
                "attribute.value": "None", "distance": 100000, "feature.anchor": ["start", "center", "end"],
                "direction": "any_direction", "internals": "False", "priority": "False"}
    keys = defaults.keys()

    try:
        query_list = config["queries"]
    except KeyError:
        query_list = [defaults]
        if not log is None:
            log.warning("No 'queries' key given, so the default values will be used: {}".format(query_list))

    if len(query_list) == 0:
        if not log is None:
            log.info('Empty queries given ("queries":[]). Will use defaults.')
        query_list = [defaults]

    if not isinstance(query_list, list):
        query_list = [query_list]

    def give_val(q):
        return map(lambda x: q[x] if x in q and q[x] != "" else defaults[x], keys)

    def make_list(l):
        return map(lambda v: [v] if not isinstance(v, list) else v, l)

    vals = map(lambda l: give_val(l), query_list)
    values = map(lambda l: make_list(l), vals)

    if not log is None:
        unknown = [k for k in config.keys() if k not in list(set(['gtf', 'bed', 'queries']).union(keys))]
        if any(unknown):
            log.warning("Unknown keys detected in configuration: {}".format(unknown))

    queries = map(lambda x: dict(zip(keys, x)), values)
    return queries


def remove_invalid_queries(queries, log=None):
    """Removes queries that have multiple attribute.filter or filter.value values and more than two distance constraints."""
    # Validate distance constraints
    has_valid_distance = map(lambda q: len(q["distance"]) < 3, queries)
    if not all(has_valid_distance) and log is not None:
        log.warning("Queries with invalid distances present! Affected queries: {}".format(
            [i for i, x in enumerate(has_valid_distance) if not x]))

    # Validate query attributes
    has_valid_attributes = map(lambda q: False if (q["filter.attribute"] != ['None'] and q["attribute.value"] == [
        'None']) or (q["filter.attribute"] == ['None'] and q["attribute.value"] != ['None']) else True, queries)

    if not all(has_valid_attributes) and log is not None:
        log.warning("Queries with invalid filter.attribute and attribute.value pairings present! Affected queries: {}".format(
            [i for i, x in enumerate(has_valid_attributes) if not x]))

    # Validate strand attribute
    has_valid_strand = map(lambda q: True if q["strand"] in [["ignore"],["same"],["opposite"]] else False, queries)

    if not all(has_valid_strand) and log is not None:
        log.warning("Queries with invalid strand values present! Affected queries: {}".format(
            [i for i, x in enumerate(has_valid_strand) if not x]))

    # Validate query attribute lengths
    has_valid_attribute_lengths = map(lambda q: False if len(
        q["filter.attribute"]) > 1 or len(q["attribute.value"]) > 1 else True, queries)
    if not all(has_valid_attribute_lengths) and log is not None:
        log.warning("Queries with more than one value for either filter.attribute or attribute.value present! Affected queries: {}".format(
            [i for i, x in enumerate(has_valid_attribute_lengths) if not x]))

    invalid_queries = list(np.unique([i for i, x in enumerate(has_valid_attributes) if not x] + [i for i, x in enumerate(
        has_valid_attribute_lengths) if not x] + [i for i, x in enumerate(has_valid_distance) if not x] + [i for i, x in enumerate(has_valid_strand) if not x]))
    return([queries[i] for i in range(0, len(queries)) if not i in invalid_queries])


def parse_first_gtf_line(gtf):
    """Removes comment lines, reads first line to check for prefix chr. Returns if chr was found and the number of columns."""
    f = open(gtf, "r")
    is_comment = True
    while is_comment:
        line = f.readline()
        is_comment = line.startswith("#")

    has_chr = line.startswith('chr')
    num_cols = len(line.split("\t"))
    return(has_chr, num_cols)


def cut_gtf_perFeat(gtf, features, prefix):
    """Removes lines with features not in features from a gtf file."""
    gtf_per_feat = prefix + os.path.basename(gtf).split(".gtf")[0] + "_cut_per_feat.gtf"
    feat2cut = np.unique(features)

    f = open(gtf, "r")
    is_comment = True
    while is_comment:
        line = f.readline()
        is_comment = line.startswith("#")

    lines = f.readlines()
    gtf_query_feat = [li for li in lines if li.split("\t")[2] in feat2cut]

    # List of lines containing only selected features from query
    with open(gtf_per_feat, "w") as cutgtf:
        cutgtf.write("".join(gtf_query_feat))
    return gtf_per_feat
