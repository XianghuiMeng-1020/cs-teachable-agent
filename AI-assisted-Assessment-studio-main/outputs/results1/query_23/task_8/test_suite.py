import pytest
from solution import PlayerScore, parse_scores

@pytest.fixture
def setup_module():
    # Setup resources needed for test if any
    yield
    # Teardown resources if any
    
@pytest.fixture
def teardown_module():
    # Teardown resources
    yield

# Test Suite

def test_single_player_multiple_scores():
    data = "Alice:5,Alice:10,Alice:3"
    players = parse_scores(data)
    assert len(players) == 1
    assert players[0].name == "Alice"
    assert players[0].get_score() == 10


def test_multiple_players_one_score_each():
    data = "Alice:5,Bob:7,Charlie:3"
    players = parse_scores(data)
    assert len(players) == 3
    alice = next(player for player in players if player.name == "Alice")
    bob = next(player for player in players if player.name == "Bob")
    charlie = next(player for player in players if player.name == "Charlie")
    assert alice.get_score() == 5
    assert bob.get_score() == 7
    assert charlie.get_score() == 3


def test_multiple_players_with_varying_scores():
    data = "Alice:5,Bob:7,Alice:15,Bob:3,Charlie:3,Bob:10"
    players = parse_scores(data)
    assert len(players) == 3
    alice = next(player for player in players if player.name == "Alice")
    bob = next(player for player in players if player.name == "Bob")
    charlie = next(player for player in players if player.name == "Charlie")
    assert alice.get_score() == 15
    assert bob.get_score() == 10
    assert charlie.get_score() == 3


def test_single_player_single_score():
    data = "Charlie:12"
    players = parse_scores(data)
    assert len(players) == 1
    assert players[0].name == "Charlie"
    assert players[0].get_score() == 12


def test_no_scores():
    data = ""
    players = parse_scores(data)
    assert len(players) == 0
