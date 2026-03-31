from program import *
import pytest
import os
from program import calculate_total_score

# Test data
file_content_1 = """10, 20, 30, 40\n15, 25, 35, 45\n5, 7, 9, 11\n"""
file_content_2 = """0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0\n"""
file_content_3 = """1, 1, 1, 1\n1, 1, 1, 1\n1, 1, 1, 1\n"""
file_content_4 = """-5, -10, -15, -20\n-25, -30, -35, -40\n-45, -50, -55, -60\n"""
file_content_5 = """12, 22, 32, 42\n52, 62, 72, 82\n92, 102, 112, 122\n32, 44, 56, 68\n"""

# Setting up and tearing down the environment for the tests

def setup_module(module):
    with open('scores.txt', 'w') as f:
        f.write(file_content_1)

def teardown_module(module):
    os.remove('scores.txt')

# Test cases

def test_total_score_1():
    with open('scores.txt', 'w') as f:
        f.write(file_content_1)
    assert calculate_total_score() == 277


def test_total_score_2():
    with open('scores.txt', 'w') as f:
        f.write(file_content_2)
    assert calculate_total_score() == 0


def test_total_score_3():
    with open('scores.txt', 'w') as f:
        f.write(file_content_3)
    assert calculate_total_score() == 12


def test_total_score_4():
    with open('scores.txt', 'w') as f:
        f.write(file_content_4)
    assert calculate_total_score() == -395


def test_total_score_5():
    with open('scores.txt', 'w') as f:
        f.write(file_content_5)
    assert calculate_total_score() == 891
