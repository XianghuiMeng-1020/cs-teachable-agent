from program import *
import pytest
import os
from program import analyze_pantheon

pantheon_file_path = 'pantheon.txt'

def setup_module(module):
    with open(pantheon_file_path, 'w') as f:
        f.write('Zeus,85\n')
        f.write('Athena,90\n')
        f.write('Hades,70\n')
        f.write('Poseidon,80\n')
        f.write('Aphrodite,75\n')

def teardown_module(module):
    try:
        os.remove(pantheon_file_path)
    except OSError:
        pass


def test_analyze_pantheon_common_case():
    result = analyze_pantheon()
    assert result == ('Hades', 'Athena', 80)


def test_analyze_pantheon_unique_min_max():
    with open(pantheon_file_path, 'w') as f:
        f.write('Artemis,100\nApollo,100\nHephaestus,60\nHestia,75\n')
    result = analyze_pantheon()
    assert result == ('Hephaestus', 'Artemis', 83)


def test_analyze_pantheon_single_entry():
    with open(pantheon_file_path, 'w') as f:
        f.write('Hermes,50\n')
    result = analyze_pantheon()
    assert result == ('Hermes', 'Hermes', 50)


def test_analyze_pantheon_multiple_same_min_max():
    with open(pantheon_file_path, 'w') as f:
        f.write('Ares,88\nDionysus,88\nHera,60\nDemeter,60\n')
    result = analyze_pantheon()
    assert result == ('Hera', 'Ares', 74)


def test_analyze_pantheon_rounding_down_average():
    with open(pantheon_file_path, 'w') as f:
        f.write('Nemesis,55\nIris,47\nThanatos,68\nHelios,92\n')
    result = analyze_pantheon()
    assert result == ('Iris', 'Helios', 65)