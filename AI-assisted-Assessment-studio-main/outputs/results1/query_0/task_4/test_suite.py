import pytest
import os
from solution import calculate_total_score

def setup_module(module):
    with open('test_game1.txt', 'w') as f:
        f.write('5,6\n3,3\n2,1\n7,9\n')
    with open('test_game2.txt', 'w') as f:
        f.write('0,0\n9,8\n3,5\n2,4\n')
    with open('test_game3.txt', 'w') as f:
        f.write('1,1\n1,2\n1,3\n1,4\n')
    with open('test_game4.txt', 'w') as f:
        f.write('9,9\n8,8\n7,7\n6,6\n')
    with open('test_game5.txt', 'w') as f:
        f.write('5,7\n3,5\n6,8\n4,2\n')


def teardown_module(module):
    os.remove('test_game1.txt')
    os.remove('test_game2.txt')
    os.remove('test_game3.txt')
    os.remove('test_game4.txt')
    os.remove('test_game5.txt')


def test_calculate_total_score_1():
    assert calculate_total_score('test_game1.txt') == 170


def test_calculate_total_score_2():
    assert calculate_total_score('test_game2.txt') == 220


def test_calculate_total_score_3():
    assert calculate_total_score('test_game3.txt') == 170


def test_calculate_total_score_4():
    assert calculate_total_score('test_game4.txt') == 400


def test_calculate_total_score_5():
    assert calculate_total_score('test_game5.txt') == 60
