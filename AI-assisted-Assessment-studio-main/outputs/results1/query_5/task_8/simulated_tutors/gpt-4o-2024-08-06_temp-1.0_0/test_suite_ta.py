from program import *
import pytest
import os
from program import calculate_wealth


pytest_files = ['mythology_ledger.txt', 'incorrect_ledger.txt']


def setup_module(module):
    with open('mythology_ledger.txt', 'w') as f:
        f.write("House of Zeus: Gold=1000, Silver=5000, Bronze=20000\n")
        f.write("House of Artemis: Gold=750, Silver=3000, Bronze=15000\n")
        f.write("House of Athena: Gold=1500, Silver=4500, Bronze=10000\n")
    
    with open('incorrect_ledger.txt', 'w') as f:
        f.write("House of Hestia: Gold=500, Bronze=1500\n")  # Missing Silver asset


def teardown_module(module):
    for filename in pytest_files:
        if os.path.exists(filename):
            os.remove(filename)
    if os.path.exists('mythology_wealth.txt'):
        os.remove('mythology_wealth.txt')


def test_calculate_wealth_basic():
    calculate_wealth()
    
    with open('mythology_wealth.txt', 'r') as f:
        lines = f.readlines()
    
    assert lines[0].strip() == "House of Zeus: 55000 Drachmaroons"
    assert lines[1].strip() == "House of Artemis: 38250 Drachmaroons"
    assert lines[2].strip() == "House of Athena: 57500 Drachmaroons"


def test_calculate_wealth_single_house():
    with open('mythology_ledger.txt', 'w') as f:
        f.write("House of Poseidon: Gold=200, Silver=1500, Bronze=10000\n")
    
    calculate_wealth()
    
    with open('mythology_wealth.txt', 'r') as f:
        lines = f.readlines()
    
    assert lines[0].strip() == "House of Poseidon: 19750 Drachmaroons"


def test_calculate_wealth_no_houses():
    with open('mythology_ledger.txt', 'w') as f:
        f.write("")  # No houses
    
    calculate_wealth()
    
    with open('mythology_wealth.txt', 'r') as f:
        lines = f.readlines()
    
    assert len(lines) == 0


def test_calculate_wealth_incorrect_format():
    with open('mythology_ledger.txt', 'w') as f:
        f.write("House of Hera: Gold=8000\n")  # Missing Silver and Bronze assets
    
    calculate_wealth()
    
    with open('mythology_wealth.txt', 'r') as f:
        lines = f.readlines()
    
    assert lines[0].strip() == "House of Hera: 80000 Drachmaroons"


def test_calculate_wealth_large_numbers():
    with open('mythology_ledger.txt', 'w') as f:
        f.write("House of Titans: Gold=1000000, Silver=2000000, Bronze=3000000\n")
    
    calculate_wealth()
    
    with open('mythology_wealth.txt', 'r') as f:
        lines = f.readlines()
    
    assert lines[0].strip() == "House of Titans: 20000000 Drachmaroons"
