from solution_program import *
import os
import pytest
from lucky_number_generator import generate_lucky_numbers

def setup_module(module):
    with open('participants.txt', 'w') as f:
        f.write(\"Alice\nBob\nCatherine\nDavid\nEve\n\")

def teardown_module(module):
    os.remove('participants.txt')
    if os.path.exists('lucky_numbers.txt'):
        os.remove('lucky_numbers.txt')

def test_lucky_number_generator_base_case():
    generate_lucky_numbers('participants.txt', 'lucky_numbers.txt')
    with open('lucky_numbers.txt', 'r') as f:
        content = f.read().strip()
    assert content == "Alice: 13\nBob: 9\nCatherine: 27\nDavid: 17\nEve: 13"

def test_empty_file():
    with open('participants.txt', 'w') as f:
        f.write("")
    generate_lucky_numbers('participants.txt', 'lucky_numbers.txt')
    with open('lucky_numbers.txt', 'r') as f:
        content = f.read().strip()
    assert content == ""

def test_single_participant():
    with open('participants.txt', 'w') as f:
        f.write("Zelda\n")
    generate_lucky_numbers('participants.txt', 'lucky_numbers.txt')
    with open('lucky_numbers.txt', 'r') as f:
        content = f.read().strip()
    assert content == "Zelda: 23"

def test_long_name():
    with open('participants.txt', 'w') as f:
        f.write("Alexandria\n")
    generate_lucky_numbers('participants.txt', 'lucky_numbers.txt')
    with open('lucky_numbers.txt', 'r') as f:
        content = f.read().strip()
    assert content == "Alexandria: 36"

def test_file_not_exist_error_handling():
    os.remove('participants.txt')
    try:
        generate_lucky_numbers('participants.txt', 'lucky_numbers.txt')
        exception_raised = False
    except FileNotFoundError:
        exception_raised = True
    assert exception_raised