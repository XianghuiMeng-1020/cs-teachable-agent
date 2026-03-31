import pytest
import os
from solution import Player, read_players_from_file

filename = "test_players.txt"

def setup_module(module):
    with open(filename, "w") as f:
        f.write("Alice,10\nBob,15\nCharlie,8\n")


def teardown_module(module):
    if os.path.exists(filename):
        os.remove(filename)


def test_player_initialization():
    player = Player("Alice", 10)
    assert player.get_details() == "Name: Alice, Score: 10"


def test_adding_score():
    player = Player("Bob", 15)
    player.add_score(5)
    assert player.get_details() == "Name: Bob, Score: 20"


def test_read_players_from_file():
    players = read_players_from_file(filename)
    assert len(players) == 3
    assert players[0].get_details() == "Name: Alice, Score: 12"
    assert players[1].get_details() == "Name: Bob, Score: 17"
    assert players[2].get_details() == "Name: Charlie, Score: 10"


def test_file_not_modified():
    with open(filename, "r") as f:
        lines = f.readlines()
    assert len(lines) == 3
    assert lines[0].strip() == "Alice,10"
    assert lines[1].strip() == "Bob,15"
    assert lines[2].strip() == "Charlie,8"


def test_empty_file():
    empty_file = "empty_test.txt"
    with open(empty_file, "w") as f:
        pass
    players = read_players_from_file(empty_file)
    assert len(players) == 0
    os.remove(empty_file)