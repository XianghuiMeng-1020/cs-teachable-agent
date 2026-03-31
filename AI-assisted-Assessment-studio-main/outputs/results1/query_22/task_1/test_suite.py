import pytest
import os
from solution_program import process_scores

def setup_module(module):
    with open('test_input1.txt', 'w') as f:
        f.write('Alice,20\nBob,15\nAlice,25\nBob,20\nCharlie,10\n')
    
    with open('test_input2.txt', 'w') as f:
        f.write('Dave,30\nErin,40\nDave,50\nErin,30\n')
        
    with open('test_input3.txt', 'w') as f:
        f.write('Fay,15\nFay,25\nFay,35\nFay,45\n')
        
    with open('test_input4.txt', 'w') as f:
        f.write('Gina,12\nHenry,13\nIan,14\nIan,15\n')


def teardown_module(module):
    os.remove('test_input1.txt')
    os.remove('test_input2.txt')
    os.remove('test_input3.txt')
    os.remove('test_input4.txt')
    os.remove('output1.txt')
    os.remove('output2.txt')
    os.remove('output3.txt')
    os.remove('output4.txt')


def test_process_scores_case1():
    process_scores('test_input1.txt', 'output1.txt')
    with open('output1.txt', 'r') as file:
        result = file.read().strip()
    assert result == 'Alice,22.5\nBob,17.5\nCharlie,10.0'


def test_process_scores_case2():
    process_scores('test_input2.txt', 'output2.txt')
    with open('output2.txt', 'r') as file:
        result = file.read().strip()
    assert result == 'Dave,40.0\nErin,35.0'


def test_process_scores_case3():
    process_scores('test_input3.txt', 'output3.txt')
    with open('output3.txt', 'r') as file:
        result = file.read().strip()
    assert result == 'Fay,30.0'


def test_process_scores_case4():
    process_scores('test_input4.txt', 'output4.txt')
    with open('output4.txt', 'r') as file:
        result = file.read().strip()
    assert result == 'Gina,12.0\nHenry,13.0\nIan,14.5'


def test_process_scores_case5_empty():
    open('empty_input.txt', 'w').close()
    process_scores('empty_input.txt', 'output5.txt')
    with open('output5.txt', 'r') as file:
        result = file.read().strip()
    assert result == ''
    os.remove('empty_input.txt')
    os.remove('output5.txt')
