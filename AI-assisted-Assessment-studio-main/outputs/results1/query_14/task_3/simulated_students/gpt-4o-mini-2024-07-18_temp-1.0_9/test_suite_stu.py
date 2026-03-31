from solution_program import *
import pytest

from solution_program import update_pantry

# Helper functions to set up or tear down any module-level setup

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_example_case():
    result = update_pantry('sugar:5,flour:10,olive oil:3', 'sugar:-2,flour:5')
    assert result == 'sugar:3,flour:15,olive oil:3'


def test_decrease_to_zero():
    result = update_pantry('sugar:5,flour:10', 'sugar:-5,flour:-2')
    assert result == 'sugar:0,flour:8'


def test_no_changes():
    result = update_pantry('sugar:5,flour:10', '')
    assert result == 'sugar:5,flour:10'


def test_increment_and_decrement():
    result = update_pantry('flour:3,sugar:2', 'flour:7,sugar:-1')
    assert result == 'flour:10,sugar:1'


def test_multiple_zero_results():
    result = update_pantry('flour:7,sugar:5,olive oil:0', 'flour:-7,sugar:-5,olive oil:0')
    assert result == 'flour:0,sugar:0,olive oil:0'
