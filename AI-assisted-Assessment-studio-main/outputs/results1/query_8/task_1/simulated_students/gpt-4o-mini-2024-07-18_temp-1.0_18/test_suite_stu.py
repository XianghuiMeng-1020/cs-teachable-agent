from solution_program import *
import pytest
from solution_program import interpret_omens

# Test startup function

def test_more_victories():
    omens = {
        'Zeus': 'Victory',
        'Hera': 'Victory',
        'Ares': 'Defeat'
    }
    assert interpret_omens(omens) == "Triumph approaches!"

def test_more_defeats():
    omens = {
        'Hades': 'Defeat',
        'Poseidon': 'Defeat',
        'Aphrodite': 'Victory'
    }
    assert interpret_omens(omens) == "Danger looms ahead!"

def test_equal_victories_defeats():
    omens = {
        'Apollo': 'Victory',
        'Athena': 'Defeat'
    }
    assert interpret_omens(omens) == "Path is uncertain"

def test_only_neutral():
    omens = {
        'Demeter': 'Neutral',
        'Dionysus': 'Neutral'
    }
    assert interpret_omens(omens) == "Path is uncertain"

def test_all_favored_same():
    omens = {
        'Hermes': 'Victory',
        'Artemis': 'Victory',
        'Apollo': 'Victory'
    }
    assert interpret_omens(omens) == "Triumph approaches!"
