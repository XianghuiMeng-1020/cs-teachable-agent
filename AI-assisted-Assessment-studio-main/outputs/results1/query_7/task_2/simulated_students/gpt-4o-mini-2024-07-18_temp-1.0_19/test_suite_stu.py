from solution_program import *
import os
import pytest
from solution_program import generate_hero_list

input_file_path = 'mythology_heroes.txt'

def setup_module(module):
    with open(input_file_path, 'w') as file:
        file.write("Perseus;Greek\n")
        file.write("Thor;Norse\n")
        file.write("Rama;Hindu\n")
        file.write("Hercules;Greek\n")
        file.write("Loki;Norse\n")


def teardown_module(module):
    os.remove(input_file_path)


def test_hero_list_normal_case():
    expected = {
        'Greek': ['Hercules', 'Perseus'],
        'Norse': ['Loki', 'Thor'],
        'Hindu': ['Rama']
    }
    assert generate_hero_list(input_file_path) == expected


def test_empty_file():
    with open(input_file_path, 'w') as file:
        file.write("")
    expected = {}
    assert generate_hero_list(input_file_path) == expected


def test_single_entry():
    with open(input_file_path, 'w') as file:
        file.write("Achilles;Greek\n")
    expected = {'Greek': ['Achilles']}
    assert generate_hero_list(input_file_path) == expected


def test_multiple_entries_single_class():
    with open(input_file_path, 'w') as file:
        file.write("Zeus;Greek\n")
        file.write("Ares;Greek\n")
    expected = {'Greek': ['Ares', 'Zeus']}
    assert generate_hero_list(input_file_path) == expected


def test_varied_class_case():
    with open(input_file_path, 'w') as file:
        file.write("Hanuman;Hindu\n")
        file.write("Krishna;Hindu\n")
        file.write("Odin;Norse\n")
    expected = {
        'Hindu': ['Hanuman', 'Krishna'],
        'Norse': ['Odin']
    }
    assert generate_hero_list(input_file_path) == expected