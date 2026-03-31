from solution_program import *
import pytest
import os

from solution_program import process_planet_data

TEST_FILE = "test_planets.txt"

def setup_module(module):
    with open(TEST_FILE, "w") as file:
        file.write("Kepler-22b 600 15\n")
        file.write("Tau-Ceti e 12 55\n")
        file.write("Gliese 581g 20 -90\n")
        file.write("Proxima Centauri b 4.24 30\n")
        file.write("TRAPPIST-1d 39 -40\n")


def teardown_module(module):
    try:
        os.remove(TEST_FILE)
    except OSError:
        pass


def test_planet_data():
    assert process_planet_data(TEST_FILE) == ["Kepler-22b", "Proxima Centauri b", "TRAPPIST-1d"]


def test_missing_file():
    assert process_planet_data("missing_file.txt") == "File Error"


def test_empty_file():
    with open("empty_file.txt", "w") as file:
        pass
    assert process_planet_data("empty_file.txt") == []


def test_all_inhabitable_planets():
    with open("inhabitable.txt", "w") as file:
        file.write("Mercury 0.387 150\n")
        file.write("Venus 0.723 462\n")
        file.write("Jupiter 5.2 -110\n")

    assert process_planet_data("inhabitable.txt") == []


def test_invalid_formatted_file():
    with open("invalid.txt", "w") as file:
        file.write("UnknownFormatData\n")
        file.write("Gliese 581g 20 -90...\n")
    assert process_planet_data("invalid.txt") == "File Error"
