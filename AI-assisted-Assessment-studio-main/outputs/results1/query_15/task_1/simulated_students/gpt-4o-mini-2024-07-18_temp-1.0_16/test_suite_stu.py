from solution_program import *
import pytest
import os
from solution_program import is_all_ids_unique

def setup_module(module):
    with open('test_file_1.txt', 'w') as f:
        f.write('ID123\nID234\nID345\nID456\n')
    with open('test_file_2.txt', 'w') as f:
        f.write('GALAXY001\nGALAXY001\nID999\n')
    with open('test_file_3.txt', 'w') as f:
        f.write('ALPHA01\nbeta02\ngamma03\n')
    with open('test_file_4.txt', 'w') as f:
        f.write('ID001\nID002\nID003\nID001\n')
    with open('test_file_5.txt', 'w') as f:
        f.write('UNIQUE1\nUNIQUE2\n')

def teardown_module(module):
    os.remove('test_file_1.txt')
    os.remove('test_file_2.txt')
    os.remove('test_file_3.txt')
    os.remove('test_file_4.txt')
    os.remove('test_file_5.txt')

def test_unique_ids():
    assert is_all_ids_unique('test_file_1.txt') == True

def test_duplicate_ids_beginning():
    assert is_all_ids_unique('test_file_2.txt') == False

def test_unique_case_sensitive_ids():
    assert is_all_ids_unique('test_file_3.txt') == True

def test_duplicate_ids_with_mismatch_case():
    assert is_all_ids_unique('test_file_4.txt') == False

def test_minimal_unique_ids():
    assert is_all_ids_unique('test_file_5.txt') == True
