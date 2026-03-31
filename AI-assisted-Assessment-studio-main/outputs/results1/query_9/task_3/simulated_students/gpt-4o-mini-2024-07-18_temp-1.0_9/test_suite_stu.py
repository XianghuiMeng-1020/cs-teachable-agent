from solution_program import *
import pytest
from solution_program import merge_god_items


def test_single_god_with_multiple_items():
    gods_list = [{'Apollo': ['lyre', 'bow', 'laurel']}]
    result = merge_god_items(gods_list)
    expected = {
        'lyre': ['Apollo'],
        'bow': ['Apollo'],
        'laurel': ['Apollo']
    }
    assert result == expected


def test_common_items_among_gods():
    gods_list = [
        {'Zeus': ['thunderbolt', 'eagle']},
        {'Athena': ['owl', 'shield', 'thunderbolt']},
        {'Ares': ['spear', 'shield']}
    ]
    result = merge_god_items(gods_list)
    expected = {
        'thunderbolt': ['Athena', 'Zeus'],
        'eagle': ['Zeus'],
        'owl': ['Athena'],
        'shield': ['Ares', 'Athena'],
        'spear': ['Ares']
    }
    assert result == expected


def test_no_items_for_some_gods():
    gods_list = [
        {'Hades': []},
        {'Poseidon': ['trident']},
        {'Dionysus': ['grape', 'wine']}  
    ]
    result = merge_god_items(gods_list)
    expected = {
        'trident': ['Poseidon'],
        'grape': ['Dionysus'],
        'wine': ['Dionysus']
    }
    assert result == expected


def test_no_gods():
    gods_list = []
    result = merge_god_items(gods_list)
    expected = {}
    assert result == expected


def test_shared_and_unique_items():
    gods_list = [
        {'Hermes': ['sandals', 'helmet']},
        {'Hephaestus': ['hammer', 'helmet']},
        {'Demeter': ['cornucopia', 'plow']}
    ]
    result = merge_god_items(gods_list)
    expected = {
        'sandals': ['Hermes'],
        'helmet': ['Hephaestus', 'Hermes'],
        'hammer': ['Hephaestus'],
        'cornucopia': ['Demeter'],
        'plow': ['Demeter']
    }
    assert result == expected
