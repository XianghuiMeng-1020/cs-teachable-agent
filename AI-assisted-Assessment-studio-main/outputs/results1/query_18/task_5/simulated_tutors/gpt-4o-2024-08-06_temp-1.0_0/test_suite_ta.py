from program import *
import pytest
import os
from program import calculate_final_weight

def setup_module(module):
    with open('test1.txt', 'w') as f:
        f.write('10\n-20\n30\n')
    with open('test2.txt', 'w') as f:
        f.write('-100\n-50\n-50\n')
    with open('test3.txt', 'w') as f:
        f.write('50\n50\n100\n')
    with open('test4.txt', 'w') as f:
        f.write('0\n0\n0\n')
    with open('test5.txt', 'w') as f:
        f.write('-20\n80\n-10\n')

def teardown_module(module):
    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')
    if os.path.exists('final_weight.txt'):
        os.remove('final_weight.txt')

@pytest.mark.parametrize("filename,expected", [
    ('test1.txt', '1020\n'),
    ('test2.txt', '800\n'),
    ('test3.txt', '1200\n'),
    ('test4.txt', '1000\n'),
    ('test5.txt', '1050\n')
])
def test_calculate_final_weight(filename, expected):
    calculate_final_weight(filename)
    with open('final_weight.txt', 'r') as f:
        result = f.read()
    assert result == expected