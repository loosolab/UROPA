import pytest
import os
import random
import unittest.mock
import json
import subprocess
import tempfile
import itertools

from uropa import uropa


# -------- Setup fixtures --------- #

@pytest.fixture
def bed():
    return os.path.join(os.path.dirname(__file__), 'data', 'hg38_peaks.bed')


@pytest.fixture
def gtf():
    return os.path.join(os.path.dirname(__file__), 'data', 'hg38.gtf')


# -------- Create different .gtf formats --------- #

gtf_default = os.path.join(os.path.dirname(__file__), 'data', 'hg38.gtf')

with open(gtf_default, 'r') as f:
    lines = f.readlines()

    # Create unsorted gtf
    random.shuffle(lines)
    with open('hg38_shuffled.gtf', 'w') as f:
        f.writelines(lines)

    # Make gtf with header line
    with open('hg38_header.gtf', 'w') as f:
        f.write('#header\n')
        f.writelines(lines)

    # Make gtf without chr prefix
    with open('hg38_no_chr.gtf', 'w') as f:
        lines_no_chr = [line.replace('chr', '') for line in lines]
        f.writelines(lines_no_chr)

    # Test gtf with long chromosomes; should shift to csi index
    with open('hg38_long_chr.gtf', 'w') as f:
        f.writelines(lines)
        f.write('chr1\t.\tgene\t1\t10000000000\t.\t+\t.\t.\n')


def run_uropa(cmd):
    """Run uropa with given command and return log."""

    cmd_list = cmd.split(' ')

    # First run uropa internally to check for coverage; will not fail
    with unittest.mock.patch("sys.argv", cmd_list):
        try:
            print("\n" + "-" * 70)  # better separation of test output when printing output
            uropa.main()
        except SystemExit:
            pass

    # Run uropa and capture output to check for correct errors raised
    # it is done like this because it is difficult to directly capture the output the uropa.main() call due to the custom logging module
    error_code = 0
    try:
        output = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        error_code = e.returncode

    return output, error_code


# -------- Standard run with different gtf files --------- #

# Standard run with no config file; only defaults of one query
@pytest.mark.parametrize('gtf', [gtf_default, 'hg38_shuffled.gtf', 'hg38_header.gtf', 'hg38_no_chr.gtf', 'hg38_long_chr.gtf'])
def test_standard_run(bed, gtf):

    # Run uropa on cmd and capture output
    log, error_code = run_uropa(f'uropa --bed {bed} --gtf {gtf}')

    # Assert that uropa finished
    assert error_code == 0
    assert "ERROR" not in log
    assert "UROPA run finished" in log

    # Check that output files were created
    output_files = ['hg38_peaks.json', 'hg38_peaks_finalhits.txt', 'hg38_peaks_finalhits.bed', 'hg38_peaks_allhits.txt', 'hg38_peaks_allhits.bed']
    for f in output_files:
        assert os.path.isfile(f)
        assert os.stat(f).st_size > 0  # assert not empty
        os.remove(f)  # remove any files created


# Test capture of invalid input
@pytest.mark.parametrize('config_dict, error_message', [({"queries": [{}]}, "No 'distance' not given in query"),  # empty query
                                                        ({"queries": [{"distance": ""}]}, "No 'distance' not given in query"),    # no distance given
                                                        ({"queries": [{"distance": "adistance"}]}, "Error trying to convert distance"),    # invalid distance given
                                                        ({"queries": [{"distance": 100, "strand": "samee"}]}, "Invalid strand"),  # invalid strand
                                                        ({"queries": [{"distance": 100, "relative_location": "downstreamm"}]}, "Invalid relative_location"),  # relative location not in query
                                                        ({"queries": [{"distance": 100, "attribute_values": ["protein_coding"]}]}, "Keys for filter_attribute/attribute_values have to be set together."),  # attribute value set without filter attribute
                                                        ({"unknown_key": "value"}, "Error in config file"),
                                                        ])
def test_invalid_config(bed, gtf, config_dict, error_message):

    temp_name = next(tempfile._get_candidate_names())
    config_file = f"{temp_name}.json"
    with open(config_file, 'w') as f:
        json.dump(config_dict, f)

    # Run uropa and capture output
    log, error_code = run_uropa(f'uropa --bed {bed} --gtf {gtf} --input {config_file} --debug')

    print(log)

    assert error_code != 0
    assert error_message in log

    # Remove config file before next text
    os.remove(config_file)


def test_by_query_option(bed, gtf):

    config_dict = {"queries": [{"distance": "1000", "feature": "gene", "name": "genes"},
                               {"distance": "1000", "feature": "exon", "name": "exons"},
                               {"distance": "100000", "feature": "exon", "feature.anchor": "center"}],
                   "output_by_query": "Y"}

    temp_name = next(tempfile._get_candidate_names())
    config_file = f"{temp_name}.json"
    with open(config_file, 'w') as f:
        json.dump(config_dict, f)

    # Run uropa and capture output
    log, error_code = run_uropa(f'uropa --bed {bed} --gtf {gtf} --input {config_file} --debug')

    print(">>>>>>" + log + "<<<<<<<<")
    assert error_code == 0
    assert "ERROR" not in log

    # Assert three outputs
    base = os.path.basename(bed).replace(".bed", "")
    output_files = []
    for suffix, query in itertools.product([".bed", ".txt"], ["allhits", "finalhits", "genes", "exons", "query_3"]):
        assert os.path.isfile(f"{base}_{query}{suffix}")
        output_files.append(f"{base}_{query}{suffix}")

    # Remove config file
    os.remove(config_file)


def test_invalid_json_format(bed, gtf):

    # Create invalid json file
    temp_name = next(tempfile._get_candidate_names())
    config_file = f"{temp_name}.json"
    with open(config_file, 'w') as f:
        f.write("{invalid json")

    # Run uropa and capture output
    log, error_code = run_uropa(f'uropa --bed {bed} --gtf {gtf} --input {config_file} --debug')

    assert error_code != 0
    assert "contains malformed JSON" in log

    # Remove config file before next text
    os.remove(config_file)
