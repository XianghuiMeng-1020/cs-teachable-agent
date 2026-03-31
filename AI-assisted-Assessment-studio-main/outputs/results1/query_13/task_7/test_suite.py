import pytest
import os

from solution import calculate_average_ingredient_weight

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write("Sugar 500 Flour\nSalt 20 Pepper 500\nOliveOil 400 Sugar 100\n")

    with open('test2.txt', 'w') as f:
        f.write("Milk 200 Cheese Sugar 300\nButter 200 Cheese\nWater 100 Honey 100\n")

    with open('test3.txt', 'w') as f:
        f.write("\n\n")

    with open('test4.txt', 'w') as f:
        f.write("Noodles 180 Rice 200\nBread\nPasta 250 Herbs 30\n")

    with open('test5.txt', 'w') as f:
        f.write("\nBread 60\nToast 90 Banana\n")


def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')


def test_calculate_average_ingredient_weight_case1():
    result = calculate_average_ingredient_weight('test1.txt')
    assert result == 333.33


def test_calculate_average_ingredient_weight_case2():
    result = calculate_average_ingredient_weight('test2.txt')
    assert result == 150.0


def test_calculate_average_ingredient_weight_case3():
    result = calculate_average_ingredient_weight('test3.txt')
    assert result is None


def test_calculate_average_ingredient_weight_case4():
    result = calculate_average_ingredient_weight('test4.txt')
    assert result == 216.67


def test_calculate_average_ingredient_weight_case5():
    result = calculate_average_ingredient_weight('test5.txt')
    assert result == 75.0
