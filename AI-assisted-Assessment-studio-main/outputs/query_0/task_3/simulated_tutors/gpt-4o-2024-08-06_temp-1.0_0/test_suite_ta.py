from program import *
import pytest
import os
from program import calculate_score

def setup_module(module):
    with open('rolls1.txt', 'w') as f:
        f.write('2\n5\n6\n3\n4\n')
    with open('rolls2.txt', 'w') as f:
        f.write('1\n1\n1\n')
    with open('rolls3.txt', 'w') as f:
        f.write('6\n6\n6\n')
    with open('rolls4.txt', 'w') as f:
        f.write('3\n4\n')
    with open('rolls5.txt', 'w') as f:
        f.write('4\n5\n2\n')

def teardown_module(module):
    files = ['rolls1.txt', 'rolls2.txt', 'rolls3.txt', 'rolls4.txt', 'rolls5.txt', 'score.txt']
    for file in files:
        if os.path.exists(file):
            os.remove(file)

@pytest.mark.parametrize("input_file, expected_output", [
    ('rolls1.txt', 36),
    ('rolls2.txt', 9),
    ('rolls3.txt', 0),
    ('rolls4.txt', 18),
    ('rolls5.txt', 19)
])
def test_calculate_score(input_file, expected_output):
    calculate_score(input_file)
    with open('score.txt', 'r') as f:
        result = int(f.read().strip())
    assert result == expected_output