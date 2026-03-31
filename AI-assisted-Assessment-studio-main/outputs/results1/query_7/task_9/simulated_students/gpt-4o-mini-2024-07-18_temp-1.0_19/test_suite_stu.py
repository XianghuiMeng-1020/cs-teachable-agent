from solution_program import *
import pytest
import os
from solution_program import process_mythology_data

input_content = '''
Pandora's Box - A story of the first woman created by Hephaestus.
Achilles' Heel - The only weakness of the Greek hero Achilles.
Cyclops - Giants with a single eye in the middle of their forehead.
The Odyssey - Epic poem attributed to Homer describing Odysseus' journey.
Philosopher's Stone - A mystical alchemical substance.
'''

expected_output = '''
BOX PANDORA'S - HEPHAESTUS. BY CREATED WOMAN FIRST THE OF STORY A
HEEL ACHILLES' - ACHILLES. HERO GREEK THE OF WEAKNESS ONLY THE
CYCLOPS - FOREHEAD. THEIR OF MIDDLE THE IN EYE SINGLE A WITH GIANTS
ODYSSEY THE - JOURNEY. ODYSSEUS' DESCRIBING HOMER TO ATTRIBUTED POEM EPIC
STONE PHILOSOPHER'S - SUBSTANCE. ALCHEMICAL MYSTICAL A
'''

@pytest.fixture(scope="module")
def setup_module():
    with open('mythology_stories.txt', 'w') as f:
        f.write(input_content)
    yield
    os.remove('mythology_stories.txt')
    os.remove('output.txt')


def test_process_mythology_data(setup_module):
    process_mythology_data('mythology_stories.txt', 'output.txt')
    with open('output.txt', 'r') as f:
        output_data = f.read()
    assert output_data.strip() == expected_output.strip()


def test_empty_file(setup_module):
    empty_file = 'empty.txt'
    with open(empty_file, 'w') as f:
        f.write('')
    output_file = 'empty_output.txt'
    process_mythology_data(empty_file, output_file)
    with open(output_file, 'r') as f:
        output_data = f.read()
    assert output_data.strip() == ''
    os.remove(empty_file)
    os.remove(output_file)


def test_single_entry(setup_module):
    single_entry_content = "Icarus - A story of hubris and the danger of flying too close to the sun."
    expected_single_output = "ICARUS - SUN. THE TO CLOSE TOO FLYING OF DANGER THE AND HUBRIS OF STORY A"
    single_file = 'single_entry.txt'
    output_file = 'single_output.txt'
    with open(single_file, 'w') as f:
        f.write(single_entry_content)
    process_mythology_data(single_file, output_file)
    with open(output_file, 'r') as f:
        output_data = f.read()
    assert output_data.strip() == expected_single_output
    os.remove(single_file)
    os.remove(output_file)


def test_no_hyphen_line(setup_module):
    no_hyphen_content = "Atlantis A legendary sunken island."
    expected_no_hyphen_output = "ATLANTIS A LEGENDARY SUNKEN ISLAND. - "
    no_hyphen_file = 'no_hyphen.txt'
    output_file = 'no_hyphen_output.txt'
    with open(no_hyphen_file, 'w') as f:
        f.write(no_hyphen_content)
    process_mythology_data(no_hyphen_file, output_file)
    with open(output_file, 'r') as f:
        output_data = f.read()
    assert output_data.strip() == expected_no_hyphen_output
    os.remove(no_hyphen_file)
    os.remove(output_file)


def test_whitespaces_around_hyphen(setup_module):
    whitespace_content = "Pegasus  -  A winged horse from Greek mythology."
    expected_whitespace_output = "PEGASUS - MYTHOLOGY. GREEK FROM HORSE WINGED A"
    whitespace_file = 'whitespace.txt'
    output_file = 'whitespace_output.txt'
    with open(whitespace_file, 'w') as f:
        f.write(whitespace_content)
    process_mythology_data(whitespace_file, output_file)
    with open(output_file, 'r') as f:
        output_data = f.read()
    assert output_data.strip() == expected_whitespace_output
    os.remove(whitespace_file)
    os.remove(output_file)
