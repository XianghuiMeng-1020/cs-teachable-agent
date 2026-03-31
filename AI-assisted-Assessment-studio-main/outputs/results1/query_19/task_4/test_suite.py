import pytest
import os
from solution import process_records

def setup_module(module):
    with open('test_input1.txt', 'w') as f:
        f.write("2023-10-23, Asteroid pass by planet Zog\n")
        f.write("New species discovery\n")
        f.write("2023-09-15, Moon eclipse observed\n")
        f.write("2023-09-31, Invalid date record\n")
        f.write("2022-06-19, Meteor shower\n")
    
    with open('test_input2.txt', 'w') as f:
        f.write("2023-05-11, Spacecraft launch\n")
        f.write("2021-02-28, Interstellar signal detected\n")
        f.write("202, Partial data\n")
        f.write("2022-12-25, Holiday record\n")
    
    with open('test_input3.txt', 'w') as f:
        f.write("2025-11-11, Galactic cloud observation\n")


def teardown_module(module):
    try:
        os.remove('test_input1.txt')
        os.remove('test_input2.txt')
        os.remove('test_input3.txt')
        os.remove('test_output1.txt')
        os.remove('test_output2.txt')
        os.remove('test_output3.txt')
    except OSError:
        pass


def test_process_records_valid_cases():
    result = process_records('test_input1.txt', 'test_output1.txt')
    assert result == 2
    with open('test_output1.txt', 'r') as f:
        records = f.readlines()
    assert records == [
        "2023-10-23, Asteroid pass by planet Zog\n",
        "2023-09-15, Moon eclipse observed\n"
    ]

def test_process_records_invalid_dates():
    result = process_records('test_input2.txt', 'test_output2.txt')
    assert result == 2
    with open('test_output2.txt', 'r') as f:
        records = f.readlines()
    assert records == [
        "2023-05-11, Spacecraft launch\n",
        "2021-02-28, Interstellar signal detected\n"
    ]


def test_process_records_all_valid():
    result = process_records('test_input3.txt', 'test_output3.txt')
    assert result == 1
    with open('test_output3.txt', 'r') as f:
        records = f.readlines()
    assert records == [
        "2025-11-11, Galactic cloud observation\n"
    ]

def test_empty_file():
    with open('test_empty.txt', 'w') as f:
        pass
    result = process_records('test_empty.txt', 'test_output_empty.txt')
    assert result == 0
    with open('test_output_empty.txt', 'r') as f:
        records = f.readlines()
    assert records == []
    os.remove('test_empty.txt')
    os.remove('test_output_empty.txt')

def test_no_valid_records():
    with open('test_no_valid.txt', 'w') as f:
        f.write("No valid data here\n")
        f.write("Invalid,\n")
        f.write(", Totally empty before comma\n")
    result = process_records('test_no_valid.txt', 'test_output_no_valid.txt')
    assert result == 0
    with open('test_output_no_valid.txt', 'r') as f:
        records = f.readlines()
    assert records == []
    os.remove('test_no_valid.txt')
    os.remove('test_output_no_valid.txt')