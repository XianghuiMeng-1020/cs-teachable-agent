from solution_program import *
import pytest
import os
from solution_program import average_energy

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write('10\n20\n30\n40\n50')
    with open('test2.txt', 'w') as f:
        f.write('5\n10')
    with open('test3.txt', 'w') as f:
        f.write('')

    # Create a file for a larger set of numbers
    with open('test4.txt', 'w') as f:
        for i in range(1, 101):  # Numbers from 1 to 100
            f.write(f'{i}\n')
    # Create a file for negative numbers
    with open('test5.txt', 'w') as f:
        f.write('-10\n-20\n-30')

def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')


def test_average_energy_case_1():
    assert average_energy('test1.txt') == 30


def test_average_energy_case_2():
    assert average_energy('test2.txt') == 7.5


def test_average_energy_case_3():
    assert average_energy('test3.txt') == 0


def test_average_energy_case_4():
    assert average_energy('test4.txt') == 50.5


def test_average_energy_case_5():
    assert average_energy('test5.txt') == -20