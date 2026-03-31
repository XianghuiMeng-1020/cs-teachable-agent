from solution_program import *
import os
import pytest
from solution_program import extract_entities

def setup_module(module):
    with open('mythology_stories.txt', 'w') as f:
        f.write('The Battle of Troy: Achilles, Zeus, Hydra\n')
        f.write("Olympus' Call: Hercules, Athena, Cerberus\n")
        f.write('Underworld Saga: Persephone, Hades, Minotaur\n')
        f.write('Quest for Fire: Prometheus, Hephaestus, Phoenix\n')
        f.write('Journey to Olympus: Odysseus, Poseidon, Cyclops\n')

def teardown_module(module):
    os.remove('mythology_stories.txt')

# Test case with example input
@pytest.mark.parametrize("file_path,expected", [
    ('mythology_stories.txt', {
        'heroes': ['Achilles', 'Hercules', 'Odysseus', 'Persephone', 'Prometheus'],
        'gods': ['Athena', 'Hades', 'Hephaestus', 'Poseidon', 'Zeus'],
        'creatures': ['Cerberus', 'Cyclops', 'Hydra', 'Minotaur', 'Phoenix']
    })
])
def test_extract_entities(file_path, expected):
    result = extract_entities(file_path)
    assert set(result['heroes']) == set(expected['heroes'])
    assert set(result['gods']) == set(expected['gods'])
    assert set(result['creatures']) == set(expected['creatures'])

@pytest.mark.parametrize("overrides,expected", [
    (lambda: [], {
        'heroes': [],
        'gods': [],
        'creatures': []
    }),
    (lambda: ['Short Story: Thor, Odin, Jormungandr\n'], {
        'heroes': [],
        'gods': ['Odin', 'Thor'],
        'creatures': ['Jormungandr']
    }),
    (lambda: ['Norse Saga: , , \n'], {
        'heroes': [],
        'gods': [],
        'creatures': []
    }),
    (lambda: ['Repeated Story: Achilles, , Hydra\n', 'Repeated Story 2: Hercules, , Hydra\n'], {
        'heroes': ['Achilles', 'Hercules'],
        'gods': [],
        'creatures': ['Hydra']
    }),
    (lambda: ['Empty Values: , , \n', 'Empty Again: , , \n'], {
        'heroes': [],
        'gods': [],
        'creatures': []
    }),
])
def test_edge_cases(overrides, expected):
    file_path = 'mythology_stories.txt'
    
    with open(file_path, 'w') as f:
        for line in overrides():
            f.write(line)
    
    result = extract_entities(file_path)
    
    assert set(result['heroes']) == set(expected['heroes'])
    assert set(result['gods']) == set(expected['gods'])
    assert set(result['creatures']) == set(expected['creatures'])

    setup_module(object())  # restore original data