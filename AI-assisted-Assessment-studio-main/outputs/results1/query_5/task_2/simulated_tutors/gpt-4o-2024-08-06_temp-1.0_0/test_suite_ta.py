from program import *
import pytest
import os
from program import demigod_tasks


def setup_module(module):
    data = (
        "HuntCreatures,mortal,3\n"
        "ChariotRace,divine,2\n"
        "FireCrafting,divine,1\n"
        "ConstructShelters,mortal,1\n"
    )
    with open("tasks.txt", "w") as f:
        f.write(data)


def teardown_module(module):
    os.remove("tasks.txt")


def test_sample_tasks():
    assert demigod_tasks("tasks.txt") == {'mortal': (2, 2), 'divine': (2, 1)}


def test_empty_file():
    with open("tasks_empty.txt", "w") as f:
        f.write("")
    assert demigod_tasks("tasks_empty.txt") == {'mortal': (0, 0), 'divine': (0, 0)}
    os.remove("tasks_empty.txt")


def test_no_mortal_tasks():
    with open("tasks_no_mortal.txt", "w") as f:
        f.write("ChariotRace,divine,2\nFireCrafting,divine,4\n")
    assert demigod_tasks("tasks_no_mortal.txt") == {'mortal': (0, 0), 'divine': (2, 3)}
    os.remove("tasks_no_mortal.txt")


def test_no_divine_tasks():
    with open("tasks_no_divine.txt", "w") as f:
        f.write("HunterQuest,mortal,5\nConstructShelters,mortal,1\n")
    assert demigod_tasks("tasks_no_divine.txt") == {'mortal': (2, 3), 'divine': (0, 0)}
    os.remove("tasks_no_divine.txt")


def test_ignore_empty_lines():
    with open("tasks_with_empty_lines.txt", "w") as f:
        f.write("\n\nSeekWisdom,divine,1\nRidePegasus,mortal,4\n\n")
    assert demigod_tasks("tasks_with_empty_lines.txt") == {'mortal': (1, 4), 'divine': (1, 1)}
    os.remove("tasks_with_empty_lines.txt")
