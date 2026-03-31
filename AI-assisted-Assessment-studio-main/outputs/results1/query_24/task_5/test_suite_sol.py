from solution_program import *
import pytest

from solution_program import calculate_final_score

def test_calculate_final_score_base_case():
    assert calculate_final_score("4,5,6,2,1,1") == 19

def test_calculate_final_score_ignore_invalid():
    assert calculate_final_score("3,6,6,8,5") == 20

def test_calculate_final_score_ignore_large_numbers():
    assert calculate_final_score("1,1,3,4,50,60,1") == 9

def test_calculate_final_score_no_invalid_numbers():
    assert calculate_final_score("3,3,3,3,3,3,3") == 21

def test_calculate_final_score_ignore_out_of_range_moves():
    assert calculate_final_score("6,6,6,6,6,6,6,3") == 99

@pytest.fixture
def setup_module():
    yield


def teardown_module():
    pass
