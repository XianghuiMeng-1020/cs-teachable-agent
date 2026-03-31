from solution_program import *
import pytest
from solution_program import play_turn

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_module():
    # This function can be used if file operations were necessary,
    # but for this task, it is not needed.
    yield

def test_empty_log():
    assert play_turn([]) == ({}, [])


def test_valid_logs():
    assert play_turn(['Alice rolls 4', 'Bob rolls 5']) == ({'Alice': 4, 'Bob': 5}, [])


def test_invalid_entries():
    assert play_turn(['Alice rolls apple', 'Charlie does 5']) == ({}, ['Alice rolls apple', 'Charlie does 5'])


def test_mixed_valid_and_invalid_entries():
    assert play_turn(['Daisy rolls 3', 'Daisy rolls 2', 'John rolls tree']) == ({'Daisy': 5}, ['John rolls tree'])


def test_multiple_players_with_invalid_entries():
    assert play_turn(['Tom rolls 10', 'Jerry rolls 0', 'Jerry rolls cat', 'Tom rolls 6']) == ({'Tom': 16, 'Jerry': 0}, ['Jerry rolls cat'])
