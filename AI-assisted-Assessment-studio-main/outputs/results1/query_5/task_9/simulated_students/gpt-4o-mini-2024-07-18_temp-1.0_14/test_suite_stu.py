from solution_program import *
import pytest
import os
from solution_program import determine_ultimate_being

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write('Dragon;100\nPhoenix;85\nUnicorn;65\nHydra;95\n')
    
    with open('test2.txt', 'w') as f:
        f.write('Minotaur;70\nGriffin;90\nSphinx;90\n')

    with open('test3.txt', 'w') as f:
        f.write('Cerberus;77\nCyclops;77\n')

    with open('test4.txt', 'w') as f:
        f.write('Kraken;120\nNaga;95\nMermaid;110\n')

    with open('test5.txt', 'w') as f:
        f.write('Basilisk;130\nMedusa;130\n')

def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')
    if os.path.exists('ultimate_being.txt'):
        os.remove('ultimate_being.txt')


def test_determine_ultimate_being_1():
    determine_ultimate_being('test1.txt')
    with open('ultimate_being.txt', 'r') as f:
        result = f.read().strip()
    assert result == 'Dragon'


def test_determine_ultimate_being_2():
    determine_ultimate_being('test2.txt')
    with open('ultimate_being.txt', 'r') as f:
        result = f.read().strip()
    assert result == "It's a draw"


def test_determine_ultimate_being_3():
    determine_ultimate_being('test3.txt')
    with open('ultimate_being.txt', 'r') as f:
        result = f.read().strip()
    assert result == "It's a draw"


def test_determine_ultimate_being_4():
    determine_ultimate_being('test4.txt')
    with open('ultimate_being.txt', 'r') as f:
        result = f.read().strip()
    assert result == 'Kraken'


def test_determine_ultimate_being_5():
    determine_ultimate_being('test5.txt')
    with open('ultimate_being.txt', 'r') as f:
        result = f.read().strip()
    assert result == "It's a draw"
