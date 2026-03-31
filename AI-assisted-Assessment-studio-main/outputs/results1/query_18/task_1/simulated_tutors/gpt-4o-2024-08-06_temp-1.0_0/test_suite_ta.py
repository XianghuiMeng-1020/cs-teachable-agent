from program import *
import os
import pytest
from program import calculate_total_energy


def setup_module(module):
    with open('quantum_energy.txt', 'w') as file:
        file.write('42 3 77')


def teardown_module(module):
    os.remove('quantum_energy.txt')
    if os.path.exists('total_energy.txt'):
        os.remove('total_energy.txt')


def test_calculate_total_energy_1():
    calculate_total_energy()
    with open('total_energy.txt', 'r') as file:
        total = int(file.read().strip())
    assert total == 122


def test_calculate_total_energy_2():
    with open('quantum_energy.txt', 'w') as file:
        file.write('1 2 3 4 5')
    calculate_total_energy()
    with open('total_energy.txt', 'r') as file:
        total = int(file.read().strip())
    assert total == 15


def test_calculate_total_energy_3():
    with open('quantum_energy.txt', 'w') as file:
        file.write('100 200 300 400 500')
    calculate_total_energy()
    with open('total_energy.txt', 'r') as file:
        total = int(file.read().strip())
    assert total == 1500


def test_calculate_total_energy_4():
    with open('quantum_energy.txt', 'w') as file:
        file.write('0')
    calculate_total_energy()
    with open('total_energy.txt', 'r') as file:
        total = int(file.read().strip())
    assert total == 0


def test_calculate_total_energy_5():
    with open('quantum_energy.txt', 'w') as file:
        file.write('10 20 -5 15 -5 10')
    calculate_total_energy()
    with open('total_energy.txt', 'r') as file:
        total = int(file.read().strip())
    assert total == 45