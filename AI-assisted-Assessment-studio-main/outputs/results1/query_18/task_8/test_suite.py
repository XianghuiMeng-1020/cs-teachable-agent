import pytest
import os
from solution import generate_energy_report

setup_data = """
Unit1,10
Unit2,20
Unit3,15
"""

empty_data = """
"""

zero_data = """
Unit1,0
Unit2,0
Unit3,0
"""

@pytest.fixture
def setup_module():
    with open('energy_data.txt', 'w') as file:
        file.write(setup_data.strip())
    yield
    teardown_module()

@pytest.fixture
def setup_empty_module():
    with open('energy_data.txt', 'w') as file:
        file.write(empty_data.strip())
    yield
    teardown_module()

@pytest.fixture
def setup_zero_module():
    with open('energy_data.txt', 'w') as file:
        file.write(zero_data.strip())
    yield
    teardown_module()

def teardown_module():
    os.remove('energy_data.txt')
    if os.path.exists('energy_report.txt'):
        os.remove('energy_report.txt')


def test_energy_report_with_data(setup_module):
    generate_energy_report('energy_data.txt', 'energy_report.txt')
    with open('energy_report.txt', 'r') as file:
        content = file.read().splitlines()
    assert content[0] == 'Total Energy: 45 kWh'
    assert content[1] == 'Average Energy: 15.00 kWh'


def test_energy_report_with_empty_data(setup_empty_module):
    generate_energy_report('energy_data.txt', 'energy_report.txt')
    with open('energy_report.txt', 'r') as file:
        content = file.read().splitlines()
    assert content[0] == 'Total Energy: 0 kWh'
    assert content[1] == 'Average Energy: 0.00 kWh'


def test_energy_report_with_zero_data(setup_zero_module):
    generate_energy_report('energy_data.txt', 'energy_report.txt')
    with open('energy_report.txt', 'r') as file:
        content = file.read().splitlines()
    assert content[0] == 'Total Energy: 0 kWh'
    assert content[1] == 'Average Energy: 0.00 kWh'


def test_energy_report_not_written_if_energy_data_is_modified():
    with open('energy_data.txt', 'w') as file:
        file.write("Unit1,10\nUnit2,20\nUnit3,-15\n")
    generate_energy_report('energy_data.txt', 'energy_report.txt')
    with open('energy_report.txt', 'r') as file:
        content = file.read().splitlines()
    assert content[0] == 'Total Energy: 15 kWh'
    assert content[1] == 'Average Energy: 5.00 kWh'


def test_energy_report_handles_perm_vari():
    with open('energy_data.txt', 'w') as file:
        file.write("Unit1,10\nUnit,20\nUnit3,15\n")
    generate_energy_report('energy_data.txt', 'energy_report.txt')
    with open('energy_report.txt', 'r') as file:
        content = file.read().splitlines()
    assert content[0] == 'Total Energy: 45 kWh'
    assert content[1] == 'Average Energy: 15.00 kWh'
