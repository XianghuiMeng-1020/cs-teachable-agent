from solution_program import *
import pytest
import os
from solution_program import calculate_points

def setup_module(module):
    with open('test_input1.txt', 'w') as f:
        f.write('abcaxyz\nzzzaaa\nabcdefgh\nxyz\n')
    with open('test_input2.txt', 'w') as f:
        f.write('aaaaaaa\nxyzaaa\n\nxyzabcaa\naaxyzaa\n')
    with open('test_input3.txt', 'w') as f:
        f.write('\n\n\n\n')
    with open('test_input4.txt', 'w') as f:
        f.write('abcdefg\na\nab\nabc\nabca\n')
    with open('test_input5.txt', 'w') as f:
        f.write('xyzxyz\nxyz\naaa\nxyz\nabcxyz\n')


def teardown_module(module):
    os.remove('test_input1.txt')
    os.remove('test_input2.txt')
    os.remove('test_input3.txt')
    os.remove('test_input4.txt')
    os.remove('test_input5.txt')
    os.remove('output1.txt')
    os.remove('output2.txt')
    os.remove('output3.txt')
    os.remove('output4.txt')
    os.remove('output5.txt')


def test_lucky_strings():
    calculate_points('test_input1.txt', 'output1.txt')
    with open('output1.txt', 'r') as f:
        assert f.read().strip() == '6\n9\n6\n4'
    
    calculate_points('test_input2.txt', 'output2.txt')
    with open('output2.txt', 'r') as f:
        assert f.read().strip() == '12\n7\n0\n11'

    calculate_points('test_input3.txt', 'output3.txt')
    with open('output3.txt', 'r') as f:
        assert f.read().strip() == '0\n0\n0\n0'

    calculate_points('test_input4.txt', 'output4.txt')
    with open('output4.txt', 'r') as f:
        assert f.read().strip() == '5\n1\n1\n1\n2'

    calculate_points('test_input5.txt', 'output5.txt')
    with open('output5.txt', 'r') as f:
        assert f.read().strip() == '8\n4\n3\n4\n7'