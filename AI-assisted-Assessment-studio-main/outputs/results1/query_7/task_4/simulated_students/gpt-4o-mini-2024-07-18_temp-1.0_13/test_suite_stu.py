from solution_program import *
import pytest
import os
from solution_program import find_creatures_by_characteristic

FILE_NAME = 'creatures.txt'

CREATURES_CONTENT = '''
Phoenix: fire, rebirth, immortal
Kraken: sea, colossal, tentacles
Sphinx: riddle, lion, human
Unicorn: magic, horse, horn
Cerberus: guard, eternal, dog
Jormungandr: sea, serpent, colossal
'''

@pytest.fixture(autouse=True)
def setup_module():
    with open(FILE_NAME, 'w') as f:
        f.write(CREATURES_CONTENT)
    yield
    os.remove(FILE_NAME)

# Test 1: Basic test with characteristic that exists for one creature only
def test_immortal_creature():
    assert find_creatures_by_characteristic(FILE_NAME, 'immortal') == ['Phoenix']

# Test 2: Characteristic that exists for more than one creature
def test_colossal_creatures():
    assert find_creatures_by_characteristic(FILE_NAME, 'colossal') == ['Kraken', 'Jormungandr']

# Test 3: Characteristic that doesn't exist in any creature
def test_nonexistent_characteristic():
    assert find_creatures_by_characteristic(FILE_NAME, 'invisible') == []

# Test 4: Ensure case sensitivity is respected
def test_case_sensitivity():
    assert find_creatures_by_characteristic(FILE_NAME, 'Fire') == []

# Test 5: Characteristic found in the middle of the list
def test_human_creature():
    assert find_creatures_by_characteristic(FILE_NAME, 'human') == ['Sphinx']
