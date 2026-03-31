import pytest
import os
from solution import find_winner

def setup_module(module):
    with open('race_results_1.txt', 'w') as f:
        f.write('Hydra,1200\n')
        f.write('Kraken,1100\n')
        f.write('Nereid,1150\n')
        f.write('Sirens,1250\n')
    with open('race_results_2.txt', 'w') as f:
        f.write('Mermaid,890\n')
        f.write('Kraken,1100\n')
        f.write('Hydra,890\n')
    with open('race_results_3.txt', 'w') as f:
        f.write('Leviathan,2000\n')
        f.write('Ceto,2100\n')
        f.write('Sirens,2000\n')
    with open('race_results_4.txt', 'w') as f:
        f.write('Cyclops,1300\n')
    with open('race_results_5.txt', 'w') as f:
        f.write('Syrenka,950\n')
        f.write('Sirens,850\n')
        f.write('Kraken,1100\n')


def teardown_module(module):
    os.remove('race_results_1.txt')
    os.remove('race_results_2.txt')
    os.remove('race_results_3.txt')
    os.remove('race_results_4.txt')
    os.remove('race_results_5.txt')


def test_find_winner_1():
    assert find_winner('race_results_1.txt') == 'Kraken'

def test_find_winner_2():
    assert find_winner('race_results_2.txt') == 'Mermaid'

def test_find_winner_3():
    assert find_winner('race_results_3.txt') == 'Leviathan'

def test_find_winner_4():
    assert find_winner('race_results_4.txt') == 'Cyclops'

def test_find_winner_5():
    assert find_winner('race_results_5.txt') == 'Sirens'
