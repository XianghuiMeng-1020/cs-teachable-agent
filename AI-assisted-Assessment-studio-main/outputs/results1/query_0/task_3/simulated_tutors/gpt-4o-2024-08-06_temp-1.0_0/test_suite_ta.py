from program import *
import pytest
import os
from program import analyze_game_results

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write('Alice,win\nBob,lose\nAlice,lose\nBob,win\nBob,lose\nAlice,win\n')
    with open('test2.txt', 'w') as f:
        f.write('Charles,win\nAlice,lose\nCharles,lose\nAlice,win\nAlice,lose\n')
    with open('test3.txt', 'w') as f:
        f.write('Dave,lose\nEve,win\nFiona,lose\nEve,lose\nFiona,win\nFiona,win\n')
    with open('test4.txt', 'w') as f:
        f.write('George,win\nHannah,lose\nGeorge,win\nGeorge,win\n')
    with open('test5.txt', 'w') as f:
        f.write('')

def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')


def test_analyze_game_results_1():
    result = analyze_game_results('test1.txt')
    assert result == 'Alice: 2-1\nBob: 1-2'


def test_analyze_game_results_2():
    result = analyze_game_results('test2.txt')
    assert result == 'Alice: 1-2\nCharles: 1-1'


def test_analyze_game_results_3():
    result = analyze_game_results('test3.txt')
    assert result == 'Dave: 0-1\nEve: 1-1\nFiona: 2-1'


def test_analyze_game_results_4():
    result = analyze_game_results('test4.txt')
    assert result == 'George: 3-0\nHannah: 0-1'


def test_analyze_game_results_empty():
    result = analyze_game_results('test5.txt')
    assert result == ''