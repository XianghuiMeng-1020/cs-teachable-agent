import os
import pytest
from solution import game_of_chance

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write("5\nwin\n10\nlose\n5\ndraw\n")

    with open('test2.txt', 'w') as f:
        f.write("6\nlose\n4\nwin\n1\nwin")

    with open('test3.txt', 'w') as f:
        f.write("5\nwin\nwin\n10\nlose\n100\nwin\n")

    with open('test4.txt', 'w') as f:
        f.write("3\nlose\n3\ndraw\n5\nwin\n")

    with open('test5.txt', 'w') as f:
        f.write("draw\n100\nwin\n3\nwin\n")


def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')
    if os.path.exists('result.txt'):
        os.remove('result.txt')


def test_game_of_chance_case1():
    game_of_chance('test1.txt')
    assert os.path.exists('result.txt')
    with open('result.txt', 'r') as f:
        assert f.read().strip() == '9'


def test_game_of_chance_case2():
    game_of_chance('test2.txt')
    assert os.path.exists('result.txt')
    with open('result.txt', 'r') as f:
        assert f.read().strip() == '11'


def test_game_of_chance_case3():
    game_of_chance('test3.txt')
    assert os.path.exists('result.txt')
    with open('result.txt', 'r') as f:
        assert f.read().strip() == '15'


def test_game_of_chance_case4():
    game_of_chance('test4.txt')
    assert os.path.exists('result.txt')
    with open('result.txt', 'r') as f:
        assert f.read().strip() == '12'


def test_game_of_chance_case5():
    game_of_chance('test5.txt')
    assert os.path.exists('result.txt')
    with open('result.txt', 'r') as f:
        assert f.read().strip() == '13'
