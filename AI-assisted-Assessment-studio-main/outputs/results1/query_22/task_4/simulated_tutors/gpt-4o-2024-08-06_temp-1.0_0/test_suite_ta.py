from program import *
import pytest
import os
from program import tally_scores

def setup_module(module):
    with open('scores1.txt', 'w') as f:
        f.write("Alice:10\nBob:15\nAlice:20\nCharlie:5\n")
    
    with open('scores2.txt', 'w') as f:
        f.write("Dan:30\nEve:25\nDan:40\nEve:35\n")
    
    with open('scores3.txt', 'w') as f:
        f.write("Frank:100\nGeorge:200\nFrank:300\nHenry:100\nGeorge:100\n")
    
    with open('scores4.txt', 'w') as f:
        f.write("Ian:10\nJack:50\nKarl:40\nJack:20\nKarl:10\n")
    
    with open('scores5.txt', 'w') as f:
        pass  # Empty file

def teardown_module(module):
    os.remove('scores1.txt')
    os.remove('scores2.txt')
    os.remove('scores3.txt')
    os.remove('scores4.txt')
    os.remove('scores5.txt')

def test_scores1():
    assert tally_scores('scores1.txt') == [('Alice', 30), ('Bob', 15), ('Charlie', 5)]

def test_scores2():
    assert tally_scores('scores2.txt') == [('Dan', 70), ('Eve', 60)]

def test_scores3():
    assert tally_scores('scores3.txt') == [('Frank', 400), ('George', 300), ('Henry', 100)]

def test_scores4():
    assert tally_scores('scores4.txt') == [('Jack', 70), ('Karl', 50), ('Ian', 10)]

def test_scores5():
    assert tally_scores('scores5.txt') == []