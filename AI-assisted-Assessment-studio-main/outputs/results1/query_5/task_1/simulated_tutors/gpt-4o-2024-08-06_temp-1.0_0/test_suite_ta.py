from program import *
import pytest
import os
from program import compute_mythical_stats

def setup_module(module):
    with open('creatures.txt', 'w') as f:
        f.write("Griffon 150\nDragon 220\nPhoenix 180\nUnicorn 160\n")


def teardown_module(module):
    os.remove('creatures.txt')
    if os.path.exists('stats.txt'):
        os.remove('stats.txt')


def test_compute_mythical_stats_normal_case():
    compute_mythical_stats('creatures.txt')
    with open('stats.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == '177.50'
    assert lines[1] == 'Dragon'
    assert lines[2] == '4'


def test_compute_mythical_stats_empty_file():
    with open('creatures.txt', 'w') as f:
        f.write("")
    compute_mythical_stats('creatures.txt')
    with open('stats.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == '0.00'
    assert lines[1] == 'None'
    assert lines[2] == '0'


def test_compute_mythical_stats_single_entry():
    with open('creatures.txt', 'w') as f:
        f.write("Sphinx 200\n")
    compute_mythical_stats('creatures.txt')
    with open('stats.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == '200.00'
    assert lines[1] == 'Sphinx'
    assert lines[2] == '1'


def test_compute_mythical_stats_identical_power_levels():
    with open('creatures.txt', 'w') as f:
        f.write("Hydra 100\nCyclops 100\nNymph 100\n")
    compute_mythical_stats('creatures.txt')
    with open('stats.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == '100.00'
    assert lines[1] == 'Hydra'  # First one with max power
    assert lines[2] == '3'


def test_compute_mythical_stats_high_power_levels():
    with open('creatures.txt', 'w') as f:
        f.write("Kraken 5000\nLeviathan 4500\nJabberwock 4700\n")
    compute_mythical_stats('creatures.txt')
    with open('stats.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    assert lines[0] == '4733.33'
    assert lines[1] == 'Kraken'
    assert lines[2] == '3'