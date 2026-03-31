import pytest
import os
from solution import run_lucky_number_game

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open('lucky_numbers.txt', 'w') as f:
        f.write("3\n17\n25\n41\n49\n")

@pytest.fixture(scope="module", autouse=True)
def teardown_module():
    yield
    os.remove('lucky_numbers.txt')

# Mocking input and output for testing
@pytest.mark.parametrize("user_input, expected_output", [
    ("3", "Congratulations! You selected a lucky number!\n"),
    ("50", "Sorry! Better luck next time.\n"),
    ("17", "Congratulations! You selected a lucky number!\n"),
    ("23", "Sorry! Better luck next time.\n"),
    ("41", "Congratulations! You selected a lucky number!\n")
])
def test_run_lucky_number_game(monkeypatch, capsys, user_input, expected_output):
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    run_lucky_number_game()
    captured = capsys.readouterr()
    assert captured.out == expected_output
