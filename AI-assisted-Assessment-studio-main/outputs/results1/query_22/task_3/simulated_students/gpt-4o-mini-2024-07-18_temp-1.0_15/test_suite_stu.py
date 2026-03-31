from solution_program import *
import pytest
import os
from solution_program import calculate_scores

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_module():
    # Setup: Create input test files
    with open('log1.txt', 'w') as f:
        f.write('Alice,Chess,15\nBob,Checkers,20\nAlice,Monopoly,25\nBob,Chess,30\nCharlie,Chess,10\nCharlie,Monopoly,5\n')
    with open('log2.txt', 'w') as f:
        f.write('David,Checkers,44\nEve,Chess,55\n')
    with open('log_empty.txt', 'w') as f:
        pass
    yield
    # Teardown: Remove test files
    os.remove('log1.txt')
    os.remove('log2.txt')
    os.remove('log_empty.txt')
    os.remove('output1.txt')
    os.remove('output2.txt')
    os.remove('output_empty.txt')

# Test cases

def test_case_1():
    calculate_scores('log1.txt', 'output1.txt')
    with open('output1.txt', 'r') as f:
        result = f.read()
    assert result == 'Alice,40\nBob,50\nCharlie,15\n'

def test_case_2():
    calculate_scores('log2.txt', 'output2.txt')
    with open('output2.txt', 'r') as f:
        result = f.read()
    assert result == 'David,44\nEve,55\n'


def test_case_3():
    calculate_scores('log_empty.txt', 'output_empty.txt')
    with open('output_empty.txt', 'r') as f:
        result = f.read()
    assert result == ''


def test_case_4():
    with open('log1.txt', 'w') as f:
        f.write('Anna,Checkers,10\nAnna,Monopoly,25\nBen,Chess,15\n')

    calculate_scores('log1.txt', 'output1.txt')
    with open('output1.txt', 'r') as f:
        result = f.read()
    assert result == 'Anna,35\nBen,15\n'


def test_case_5():
    with open('log2.txt', 'w') as f:
        f.write('Carrie,Chess,50\nFrank,Checkers,40\n')

    calculate_scores('log2.txt', 'output2.txt')
    with open('output2.txt', 'r') as f:
        result = f.read()
    assert result == 'Carrie,50\nFrank,40\n'
