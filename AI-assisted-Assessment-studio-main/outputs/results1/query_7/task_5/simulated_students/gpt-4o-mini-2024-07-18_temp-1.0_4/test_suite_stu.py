from solution_program import *
import os
import pytest
from solution_program import extract_artifacts

input_file = 'mythology_data.txt'
output_file = 'artifacts.txt'

def setup_module(module):
    with open(input_file, 'w') as f:
        f.write("Zeus;Thunderbolt;Eagle;Aegis\n")
        f.write("Hera;Peacock Feather;Diadem\n")
        f.write("Athena;Spear;Shield;Owl\n")
        f.write("Apollo;Lyre;Laurel\n")
        f.write("Hades;Bident;Cerberus;Helm of Darkness\n")

def teardown_module(module):
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)

@pytest.mark.parametrize("expected_content", [
    ["Aegis", "Bident", "Cerberus", "Diadem", "Eagle", "Helm of Darkness", "Laurel", "Lyre", "Owl", "Peacock Feather", "Spear", "Shield", "Thunderbolt"],
])
def test_extract_artifacts(expected_content):
    extract_artifacts(input_file)
    with open(output_file, 'r') as f:
        lines = f.readlines()
        assert lines == [line + "\n" for line in expected_content]

@pytest.mark.parametrize("new_data, expected_content", [
    ("Athena;Helmet\n", 
     ["Aegis", "Bident", "Cerberus", "Diadem", "Eagle", "Helmet", "Helm of Darkness", "Laurel", "Lyre", "Owl", "Peacock Feather", "Spear", "Shield", "Thunderbolt"]),
    ("Hermes;Caduceus\n", 
     ["Aegis", "Bident", "Caduceus", "Cerberus", "Diadem", "Eagle", "Helm of Darkness", "Laurel", "Lyre", "Owl", "Peacock Feather", "Spear", "Shield", "Thunderbolt"]),
    ("Aphrodite;Girdle;Dove\n", 
     ["Aegis", "Bident", "Cerberus", "Diadem", "Dove", "Eagle", "Girdle", "Helm of Darkness", "Laurel", "Lyre", "Owl", "Peacock Feather", "Spear", "Shield", "Thunderbolt"]),
    ("Poseidon;Trident\n", 
     ["Aegis", "Bident", "Cerberus", "Diadem", "Eagle", "Helm of Darkness", "Laurel", "Lyre", "Owl", "Peacock Feather", "Spear", "Shield", "Thunderbolt", "Trident"]),
])
def test_extract_artifacts_with_new_data(new_data, expected_content):
    with open(input_file, 'a') as f:
        f.write(new_data)
    extract_artifacts(input_file)
    with open(output_file, 'r') as f:
        lines = f.readlines()
        assert lines == [line + "\n" for line in expected_content]