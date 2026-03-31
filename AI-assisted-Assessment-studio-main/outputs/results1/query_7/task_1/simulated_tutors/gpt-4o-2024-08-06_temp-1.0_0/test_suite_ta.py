from program import *
import pytest
import os
from program import find_creatures_by_attribute

MYTHICAL_CREATURES_CONTENT = '''
Minotaur: A creature with the body of a man and the head of a bull.
Attributes: labyrinth, beast, angry

Medusa: A Gorgon with snakes for hair.
Attributes: petrifying, snake

Hydra: A many-headed serpent.
Attributes: regenerating, water

Phoenix: The immortal bird that regenerates from ashes.
Attributes: fire, immortal

Cerberus: The multi-headed dog guarding the underworld.
Attributes: dog, underworld, watchful
'''

FILE_NAME = 'mythical_creatures.txt'


def setup_module(module):
    with open(FILE_NAME, 'w') as file:
        file.write(MYTHICAL_CREATURES_CONTENT)


def teardown_module(module):
    os.remove(FILE_NAME)


def test_find_creatures_by_attribute_snake():
    result = find_creatures_by_attribute(FILE_NAME, 'snake')
    assert result == ['Medusa']


def test_find_creatures_by_attribute_water():
    result = find_creatures_by_attribute(FILE_NAME, 'water')
    assert result == ['Hydra']


def test_find_creatures_by_attribute_immortal():
    result = find_creatures_by_attribute(FILE_NAME, 'immortal')
    assert result == ['Phoenix']


def test_find_creatures_by_attribute_dog():
    result = find_creatures_by_attribute(FILE_NAME, 'dog')
    assert result == ['Cerberus']


def test_find_creatures_by_attribute_nonexistent():
    result = find_creatures_by_attribute(FILE_NAME, 'flying')
    assert result == []