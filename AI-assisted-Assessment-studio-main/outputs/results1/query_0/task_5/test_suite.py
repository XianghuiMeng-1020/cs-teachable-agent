import pytest
import os
from solution import play_game_of_chance

def setup_module(module):
    with open('words.txt', 'w') as f:
        f.write("apple\nbanana\ncherry\n")


def teardown_module(module):
    if os.path.exists('words.txt'):
        os.remove('words.txt')
    if os.path.exists('game_results.txt'):
        os.remove('game_results.txt')


def test_correct_guess(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "cherry")
    with open('words.txt', 'r') as f:
        selected_word = f.readlines()[2].strip()
    play_game_of_chance()
    with open('game_results.txt', 'r') as f:
        result = f.readline().strip()
    assert result == f"cherry won"


def test_incorrect_guess(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "banana")
    with open('words.txt', 'r') as f:
        selected_word = f.readlines()[2].strip()
    play_game_of_chance()
    with open('game_results.txt', 'r') as f:
        result = f.readline().strip()
    assert result == f"banana lost"


def test_output_correct(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda: "apple")
    with open('words.txt', 'r') as f:
        selected_word = f.readlines()[0].strip()
    play_game_of_chance()    
    captured = capsys.readouterr()
    assert "Correct! You've won!" in captured.out


def test_output_incorrect(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda: "pear")
    with open('words.txt', 'r') as f:
        selected_word = f.readlines()[1].strip()
    play_game_of_chance()
    captured = capsys.readouterr()
    assert "Incorrect! Try again another time!" in captured.out


def test_results_file_created(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "apple")
    play_game_of_chance()
    assert os.path.exists('game_results.txt')