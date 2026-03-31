import pytest
import os
from solution import play_game


def setup_module(module):
    with open('test_file.txt', 'w') as f:
        f.write("Alice:3\nBob:5\nCharlie:2")


def teardown_module(module):
    os.remove('test_file.txt')


def test_play_game_win_case():
    play_game('test_file.txt')
    with open('test_file.txt', 'r') as f:
        content = f.read().strip()
    assert 'Bob:win' in content


def test_play_game_lose_case():
    play_game('test_file.txt')
    with open('test_file.txt', 'r') as f:
        content = f.read().strip()
    assert 'Alice:lose' in content


def test_play_game_multiple_lines():
    play_game('test_file.txt')
    with open('test_file.txt', 'r') as f:
        lines = f.readlines()
    assert len(lines) == 3


def test_play_game_format():
    play_game('test_file.txt')
    with open('test_file.txt', 'r') as f:
        content = f.read().strip()
    assert ':' in content.split('\n')[0]
    

def test_play_game_original_content_replacement():
    play_game('test_file.txt')
    with open('test_file.txt', 'r') as f:
        content = f.read().strip()
    assert 'Charlie:lose' in content