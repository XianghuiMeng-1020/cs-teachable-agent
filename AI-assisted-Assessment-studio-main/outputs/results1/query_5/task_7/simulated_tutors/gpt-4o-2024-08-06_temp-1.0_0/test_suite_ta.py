from program import *
import pytest
import os
from program import mythical_creature_stats

# Setup module for creating input test files

def setup_module(module):
    with open('test_input_1.txt', 'w') as f:
        f.write('Hydra,3,300\n')
        f.write('Cerberus,2,150\n')
        f.write('Hydra,2,200\n')

    with open('test_input_2.txt', 'w') as f:
        f.write('Griffin,5,250\n')
        f.write('Phoenix,4,400\n')
        f.write('Griffin,2,100\n')
        f.write('Kraken,1,500\n')
        f.write('Phoenix,2,200\n')

    with open('test_input_3.txt', 'w') as f:
        f.write('Minotaur,1,100\n')

    with open('test_input_4.txt', 'w') as f:
        f.write('Dragon,4,1200\n')
        f.write('Dragon,3,600\n')
        f.write('Dragon,7,2100\n')

    with open('test_input_5.txt', 'w') as f:
        f.write('Cyclops,7,280\n')
        f.write('Cyclops,3,120\n')
        f.write('Cyclops,5,500\n')

def teardown_module(module):
    os.remove('test_input_1.txt')
    os.remove('test_input_2.txt')
    os.remove('test_input_3.txt')
    os.remove('test_input_4.txt')
    os.remove('test_input_5.txt')
    os.remove('output_1.txt')
    os.remove('output_2.txt')
    os.remove('output_3.txt')
    os.remove('output_4.txt')
    os.remove('output_5.txt')


def test_mythical_creature_stats_1():
    mythical_creature_stats('test_input_1.txt', 'output_1.txt')
    with open('output_1.txt', 'r') as f:
        content = f.readlines()
    assert 'Hydra,5,100.00\n' in content
    assert 'Cerberus,2,75.00\n' in content


def test_mythical_creature_stats_2():
    mythical_creature_stats('test_input_2.txt', 'output_2.txt')
    with open('output_2.txt', 'r') as f:
        content = f.readlines()
    assert 'Griffin,7,50.00\n' in content
    assert 'Phoenix,6,100.00\n' in content
    assert 'Kraken,1,500.00\n' in content


def test_mythical_creature_stats_3():
    mythical_creature_stats('test_input_3.txt', 'output_3.txt')
    with open('output_3.txt', 'r') as f:
        content = f.readlines()
    assert 'Minotaur,1,100.00\n' in content


def test_mythical_creature_stats_4():
    mythical_creature_stats('test_input_4.txt', 'output_4.txt')
    with open('output_4.txt', 'r') as f:
        content = f.readlines()
    assert 'Dragon,14,150.00\n' in content


def test_mythical_creature_stats_5():
    mythical_creature_stats('test_input_5.txt', 'output_5.txt')
    with open('output_5.txt', 'r') as f:
        content = f.readlines()
    assert 'Cyclops,15,60.00\n' in content
