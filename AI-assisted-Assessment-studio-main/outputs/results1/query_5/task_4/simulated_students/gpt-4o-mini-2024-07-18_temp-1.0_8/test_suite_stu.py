from solution_program import *
import pytest
import os
from mythology_challenge import get_strengthiest_beast

def setup_module(module):
    with open('mythological_beasts.txt', 'w') as f:
        f.write('Dragon,300\nHydra,250\nPhoenix,300\n')

def teardown_module(module):
    os.remove('mythological_beasts.txt')

def test_example_case():
    assert get_strengthiest_beast('mythological_beasts.txt') == 'Dragon'

def test_empty_file():
    with open('mythological_beasts.txt', 'w') as f:
        f.write('')
    assert get_strengthiest_beast('mythological_beasts.txt') == ''

def test_single_beast():
    with open('mythological_beasts.txt', 'w') as f:
        f.write('Minotaur,450\n')
    assert get_strengthiest_beast('mythological_beasts.txt') == 'Minotaur'

def test_multiple_max_strength():
    with open('mythological_beasts.txt', 'w') as f:
        f.write('Unicorn,200\nDragon,500\nHydra,500\n')
    assert get_strengthiest_beast('mythological_beasts.txt') == 'Dragon'

def test_large_numbers():
    with open('mythological_beasts.txt', 'w') as f:
        f.write('Kraken,999999\nLeviathan,1000000\nBehemoth,999999\n')
    assert get_strengthiest_beast('mythological_beasts.txt') == 'Leviathan'
