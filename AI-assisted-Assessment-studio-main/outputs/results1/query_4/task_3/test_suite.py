import pytest
from random import seed, randint
from my_game_module import simulate_game

seed(42)  # Seed the random process to ensure reproducible results

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_module():
    # Setup before the tests
    yield
    # Teardown after tests


def test_single_die_each_player():
    players = {
        "Alice": [6],  # Die rolls: [6]
        "Bob": [4],    # Die rolls: [1]
        "Charlie": [8] # Die rolls: [1]
    }
    assert simulate_game(players) == "Alice"


def test_multiple_dice_one_winner():
    players = {
        "Alice": [6, 6],          # Possible rolls: [1, 3] sum=4
        "Bob": [4, 10, 12],       # Possible rolls: [3, 2, 3] sum=8
        "Charlie": [4, 4, 4],     # Possible rolls: [2, 4, 1] sum=7
        "David": [10, 8]          # Possible rolls: [5, 7] sum=12
    }
    assert simulate_game(players) == "David"


def test_tie_scenario():
    players = {
        "Alice": [6],          # Die roll: [4]
        "Bob": [6],            # Die roll: [4]
        "Charlie": [6]         # Die roll: [4]
    }
    assert simulate_game(players) == "Tie"


def test_no_dice():
    players = {
        "Alice": [],           # No die
        "Bob": []              # No die
    }
    assert simulate_game(players) == "Tie"


def test_mixture_of_dice_and_sides():
    players = {
        "Alice": [20, 6],             # Possible rolls: [10, 5] sum=15
        "Bob": [4, 6, 8, 10],        # Possible rolls: [2, 4, 8, 1] sum=15 
        "Charlie": [10, 10, 6]       # Possible rolls: [4, 5, 6] sum=15
    }
    assert simulate_game(players) == "Tie"
