from program import *
import pytest
import os
from program import MythicalLibrary

def setup_module(module):
    creatures_info = [
        "Phoenix, Greek, A long-lived bird that regenerates or is reborn.",
        "Dragon, Various, A large serpent-like monster.",
        "Centaurs, Greek, Half-human, half-horse creatures.",
        "Yeti, Himalayan, An ape-like entity.",
        "Anubis, Egyptian, God of death associated with a dog.",
    ]
    with open('mythical_creatures.txt', 'w') as f:
        f.write("\n".join(creatures_info) + "\n")

def teardown_module(module):
    try:
        os.remove('mythical_creatures.txt')
    except FileNotFoundError:
        pass


def test_get_description_existing_creature():
    lib = MythicalLibrary()
    assert lib.get_description("Phoenix") == "A long-lived bird that regenerates or is reborn."


def test_get_description_non_existing_creature():
    lib = MythicalLibrary()
    assert lib.get_description("Unicorn") == "Creature not found"


def test_add_creature_new():
    lib = MythicalLibrary()
    result = lib.add_creature("Unicorn", "Western", "A legendary horse with a horn.")
    assert result is None
    assert lib.get_description("Unicorn") == "A legendary horse with a horn."


def test_add_creature_existing():
    lib = MythicalLibrary()
    result = lib.add_creature("Phoenix", "Greek", "Mystical bird.")
    assert result == "Creature already exists"


def test_get_creatures_by_origin():
    lib = MythicalLibrary()
    assert set(lib.get_creatures_by_origin("Greek")) == {"Phoenix", "Centaurs"}