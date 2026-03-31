from solution_program import *
import pytest
import os
from solution_program import manage_high_scores

def setup_module(module):
    with open('high_scores.txt', 'w') as f:
        f.write("Alice 100\n")
        f.write("Bob 90\n")
        f.write("Charlie 80\n")

def teardown_module(module):
    os.remove('high_scores.txt')

@pytest.mark.parametrize("new_scores, expected", [
    ([('Bob', 95)], "Alice 100\nBob 95\nCharlie 80\n"),
    ([('Dave', 85)], "Alice 100\nBob 90\nCharlie 80\nDave 85\n"),
    ([('Charlie', 82), ('Eve', 60)], "Alice 100\nCharlie 82\nBob 90\nDave 85\n"),
    ([('Charlie', 75)], "Alice 100\nBob 90\nCharlie 80\n"),
    ([('Alice', 101)], "Alice 101\nBob 90\nCharlie 80\n")
])
def test_manage_high_scores(new_scores, expected):
    manage_high_scores('high_scores.txt', new_scores)
    with open('high_scores.txt', 'r') as f:
        contents = f.read()
    assert contents == expected