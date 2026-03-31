import pytest
import os
from solution import calculate_total_distance

def setup_module(module):
    with open('test_file1.txt', 'w') as f:
        f.write("Mars 225.0\nJupiter 483.8\nSaturn 886.7\n")
        
    with open('test_file2.txt', 'w') as f:
        f.write("AlphaCentauri 4.37\nBetelgeuse 642.5\nProximaCentauri 4.24\n")
        
    with open('test_file3.txt', 'w') as f:
        f.write("Andromeda 2537000.0\nMilkyWay 0.0\n")
    
    with open('test_empty.txt', 'w') as f:
        f.write("")
        
    with open('test_single_line.txt', 'w') as f:
        f.write("Vulcan 16.5\n")

def teardown_module(module):
    os.remove('test_file1.txt')
    os.remove('test_file2.txt')
    os.remove('test_file3.txt')
    os.remove('test_empty.txt')
    os.remove('test_single_line.txt')


def test_calculate_total_distance_file1():
    assert calculate_total_distance('test_file1.txt') == 1595


def test_calculate_total_distance_file2():
    assert calculate_total_distance('test_file2.txt') == 650


def test_calculate_total_distance_file3():
    assert calculate_total_distance('test_file3.txt') == 2537000


def test_calculate_total_distance_empty():
    assert calculate_total_distance('test_empty.txt') == 0


def test_calculate_total_distance_single_line():
    assert calculate_total_distance('test_single_line.txt') == 17
