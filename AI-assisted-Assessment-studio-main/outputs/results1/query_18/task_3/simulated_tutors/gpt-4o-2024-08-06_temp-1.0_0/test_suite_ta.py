from program import *
import pytest
import os
from program import calculate_fuel_for_mission

def setup_module(module):
    with open('missions1.txt', 'w') as f:
        f.write("10\n20\n15\n")
    with open('missions2.txt', 'w') as f:
        f.write("5\n50\n25\n10\n")
    with open('missions3.txt', 'w') as f:
        f.write("100\n200\n300\n")
    with open('missions4.txt', 'w') as f:
        f.write("0\n0\n0\n0\n0\n")
    with open('missions5.txt', 'w') as f:
        f.write("1\n1\n1\n1\n")


def teardown_module(module):
    os.remove('missions1.txt')
    os.remove('missions2.txt')
    os.remove('missions3.txt')
    os.remove('missions4.txt')
    os.remove('missions5.txt')
    if os.path.exists('total_fuel.txt'):
        os.remove('total_fuel.txt')


def test_calculate_fuel_for_mission_case1():
    calculate_fuel_for_mission('missions1.txt')
    assert os.path.exists('total_fuel.txt')
    with open('total_fuel.txt', 'r') as f:
        assert int(f.read().strip()) == 90


def test_calculate_fuel_for_mission_case2():
    calculate_fuel_for_mission('missions2.txt')
    assert os.path.exists('total_fuel.txt')
    with open('total_fuel.txt', 'r') as f:
        assert int(f.read().strip()) == 180


def test_calculate_fuel_for_mission_case3():
    calculate_fuel_for_mission('missions3.txt')
    assert os.path.exists('total_fuel.txt')
    with open('total_fuel.txt', 'r') as f:
        assert int(f.read().strip()) == 1200


def test_calculate_fuel_for_mission_case4():
    calculate_fuel_for_mission('missions4.txt')
    assert os.path.exists('total_fuel.txt')
    with open('total_fuel.txt', 'r') as f:
        assert int(f.read().strip()) == 0


def test_calculate_fuel_for_mission_case5():
    calculate_fuel_for_mission('missions5.txt')
    assert os.path.exists('total_fuel.txt')
    with open('total_fuel.txt', 'r') as f:
        assert int(f.read().strip()) == 8
