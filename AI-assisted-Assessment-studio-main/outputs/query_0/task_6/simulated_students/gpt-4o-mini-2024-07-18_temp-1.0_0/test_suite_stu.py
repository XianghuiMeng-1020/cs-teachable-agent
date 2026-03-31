from solution_program import *
import pytest
import os
from your_solution_file import play_lucky_guess

SECRET_FILE = 'secret_number.txt'

@pytest.fixture
def setup_module():
    with open(SECRET_FILE, 'w') as f:
        f.write('50')  # Let's assume the secret number is 50


yield

    os.remove(SECRET_FILE)


def test_correct_guess(setup_module, tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("50\n")
    play_lucky_guess(input_file, output_file)

    assert output_file.read_text() == "correct\n"


def test_multiple_guesses(setup_module, tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("20\n40\n50\n")
    play_lucky_guess(input_file, output_file)

    assert output_file.read_text() == "too low\ntoo low\ncorrect\n"


def test_first_guess_correct(setup_module, tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("50\n60\n70\n")
    play_lucky_guess(input_file, output_file)

    assert output_file.read_text() == "correct\n"


def test_all_high_guesses(setup_module, tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("60\n70\n80\n")
    play_lucky_guess(input_file, output_file)

    assert output_file.read_text() == "too high\ntoo high\ntoo high\n"


def test_all_low_guesses(setup_module, tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("10\n20\n30\n")
    play_lucky_guess(input_file, output_file)

    assert output_file.read_text() == "too low\ntoo low\ntoo low\n"


@pytest.fixture(scope="function")
def teardown_module():
    pass