import pytest
import os
from solution import calculate_total_consumption

def setup_module(module):
    with open('test_input1.txt', 'w') as f:
        f.write("Earth 15000\nMars 12000\nJupiter 30000\n")
    
    with open('test_input2.txt', 'w') as f:
        f.write("Venus 5000\nNeptune 7000\nUranus 10000\n")

    with open('test_input3.txt', 'w') as f:
        f.write("Pluto 500\n")

    with open('test_input4.txt', 'w') as f:
        f.write("Mercury 30000\nVenus 2000\nEarth 1000\nMars 5000\n")

    with open('test_input5.txt', 'w') as f:
        f.write("Earth 0\nMars 0\nJupiter 0\n")


def teardown_module(module):
    os.remove('test_input1.txt')
    os.remove('test_input2.txt')
    os.remove('test_output1.txt')
    os.remove('test_output2.txt')
    os.remove('test_output3.txt')
    os.remove('test_output4.txt')
    os.remove('test_output5.txt')
    os.remove('test_input3.txt')
    os.remove('test_input4.txt')
    os.remove('test_input5.txt')


def test_calculate_total_consumption_case1():
    calculate_total_consumption('test_input1.txt', 'test_output1.txt')
    with open('test_output1.txt', 'r') as f:
        content = f.read().strip()
    assert content == '57000'


def test_calculate_total_consumption_case2():
    calculate_total_consumption('test_input2.txt', 'test_output2.txt')
    with open('test_output2.txt', 'r') as f:
        content = f.read().strip()
    assert content == '22000'


def test_calculate_total_consumption_single_line():
    calculate_total_consumption('test_input3.txt', 'test_output3.txt')
    with open('test_output3.txt', 'r') as f:
        content = f.read().strip()
    assert content == '500'


def test_calculate_total_consumption_with_multiple_lines():
    calculate_total_consumption('test_input4.txt', 'test_output4.txt')
    with open('test_output4.txt', 'r') as f:
        content = f.read().strip()
    assert content == '38000'


def test_calculate_total_consumption_all_zero():
    calculate_total_consumption('test_input5.txt', 'test_output5.txt')
    with open('test_output5.txt', 'r') as f:
        content = f.read().strip()
    assert content == '0'