from solution_program import *
import pytest
import os
from solution_program import calculate_scores

filename = "tournament.txt"

def setup_module(module):
    with open(filename, 'w') as file:
        file.write("")

def teardown_module(module):
    os.remove(filename)

@pytest.mark.parametrize("file_contents, expected_result", [
    ("Alice Bob win\nBob Charlie win\n", [("Alice", 1), ("Bob", 1)]),
    ("Alice Bob win\nAlice Charlie win\nCharlie Alice lose\n", [("Alice", 3)]),
    ("Bob Alice win\nAlice Bob win\nCharlie Bob lose\n", [("Bob", 2), ("Alice", 1)]),
    ("", []),
    ("Alice Bob win\nBob Alice lose\nCharlie Bob win\n", [("Alice", 2), ("Bob", 1)])
])
def test_calculate_scores(file_contents, expected_result):
    with open(filename, 'w') as file:
        file.write(file_contents)

    assert calculate_scores(filename) == expected_result