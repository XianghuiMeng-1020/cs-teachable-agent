from program import *
import pytest
import os
from program import analyze_myths

input_filename = 'test_myth_stories.txt'
output_filename = 'output_myth_analysis.txt'


def setup_module(module):
    with open(input_filename, 'w') as f:
        f.write("Zeus thundered his command in Olympus\n")
        f.write("Athena the wise goddess assisted Zeus\n")
        f.write("The mighty Thor wielded his hammer\n")
        f.write("The legend of the phoenix rises from ashes\n")
        f.write("Phoenix is a legendary bird that rises from ashes\n")
        f.write("In the realm of myth Hercules is a hero\n")


def teardown_module(module):
    os.remove(input_filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)


def test_analyze_myths_case1():
    analyze_myths(input_filename, output_filename)
    with open(output_filename, 'r') as f:
        lines = f.readlines()
    assert lines == ['Zeus 1\n', 'Zeus 2\n', 'The 1\n', 'The 1\n', 'Phoenix 1\n', 'In 1\n']


def test_analyze_myths_case2():
    with open(input_filename, 'w') as f:
        f.write("Zeus Zeus Zeus\n")
        f.write("Zeus Zeus Athena Athena Athena\n")
        f.write("\n")  # Test empty line
    analyze_myths(input_filename, output_filename)
    with open(output_filename, 'r') as f:
        lines = f.readlines()
    assert lines == ['Zeus 3\n', 'Zeus 3\n', '\n']


def test_analyze_myths_case3():
    with open(input_filename, 'w') as f:
        f.write("Hades Hades Poseidon Poseidon Poseidon\n")
        f.write("Apollo Apollo Apollo\n")
    analyze_myths(input_filename, output_filename)
    with open(output_filename, 'r') as f:
        lines = f.readlines()
    assert lines == ['Poseidon 3\n', 'Apollo 3\n']


def test_analyze_myths_case4():
    with open(input_filename, 'w') as f:
        f.write("Athena Hera Hera Athena\n")
        f.write("Hermes Hermes Hermes Hermes\n")
    analyze_myths(input_filename, output_filename)
    with open(output_filename, 'r') as f:
        lines = f.readlines()
    assert lines == ['Athena 2\n', 'Hermes 4\n']


def test_analyze_myths_case5():
    with open(input_filename, 'w') as f:
        f.write("Chaos Chaos Gaia Gaia Gaia Eros\n")
        f.write("Aphrodite Aphrodite Hades\n")
    analyze_myths(input_filename, output_filename)
    with open(output_filename, 'r') as f:
        lines = f.readlines()
    assert lines == ['Gaia 3\n', 'Aphrodite 2\n']
