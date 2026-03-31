from program import *
import pytest
import os
from program import save_lottery_results, check_ticket


def setup_module(module):
    with open('test_results.txt', 'w') as f:
        f.writelines("A1B2C3D\n111222C\nAB12CD3\nZZZ9999\n1234567\n")


def teardown_module(module):
    if os.path.exists('test_results.txt'):
        os.remove('test_results.txt')


def test_save_lottery_results():
    test_data = ['ABCDE12', 'XYZ9999', 'QWE1234']
    save_lottery_results('test_save.txt', test_data)
    with open('test_save.txt', 'r') as f:
        lines = f.read().splitlines()
    assert lines == test_data
    os.remove('test_save.txt')


def test_check_ticket_winning():
    assert check_ticket('test_results.txt', 'A1B2C3D') == True

    
def test_check_ticket_non_winning():
    assert check_ticket('test_results.txt', 'NOTWIN') == False


def test_check_ticket_another_winning():
    assert check_ticket('test_results.txt', 'AB12CD3') == True


def test_check_ticket_case_sensitivity():
    assert check_ticket('test_results.txt', 'zzZ9999') == True