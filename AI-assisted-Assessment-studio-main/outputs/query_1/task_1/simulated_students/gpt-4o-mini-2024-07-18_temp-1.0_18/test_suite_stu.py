from solution_program import *
import pytest
from solution_program import mythical_quest


def test_basic_distribution():
    assert mythical_quest([
        ['Ares', 'Advanced'],
        ['Perseus', 'Intermediate'],
        ['Hercules', 'Novice']
    ], 10) == [('Ares', 7), ('Perseus', 3), ('Hercules', 0)]


def test_more_artifacts():
    assert mythical_quest([
        ['Zeus', 'Advanced'],
        ['Athena', 'Intermediate'],
        ['Apollo', 'Intermediate'],
        ['Hermes', 'Novice']
    ], 20) == [('Zeus', 7), ('Athena', 3), ('Apollo', 3), ('Hermes', 1)]


def test_just_enough():
    assert mythical_quest([
        ['Hades', 'Advanced'],
        ['Artemis', 'Intermediate'],
        ['Dionysus', 'Novice']
    ], 11) == [('Hades', 7), ('Artemis', 3), ('Dionysus', 1)]


def test_not_enough_allocation():
    assert mythical_quest([
        ['Hera', 'Advanced'],
        ['Demeter', 'Advanced'],
        ['Ares', 'Intermediate']
    ], 14) == [('Hera', 7), ('Demeter', 7), ('Ares', 0)]


def test_only_one_hero():
    assert mythical_quest([
        ['Helios', 'Novice']
    ], 5) == [('Helios', 1)]