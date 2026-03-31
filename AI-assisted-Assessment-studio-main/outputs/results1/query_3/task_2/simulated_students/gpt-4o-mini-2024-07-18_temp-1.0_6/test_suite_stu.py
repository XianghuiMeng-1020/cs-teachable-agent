from solution_program import *
import pytest
from solution_program import play_game_of_chance

@pytest.mark.parametrize("strategy,expected_outcomes", [
    ({'win': 100, 'lose': 50}, [{'result': 'win', 'balance': 100}, {'result': 'lose', 'balance': -50}]),
    ({'win': 200, 'lose': 150}, [{'result': 'win', 'balance': 200}, {'result': 'lose', 'balance': -150}]),
    ({'win': 0, 'lose': 0}, [{'result': 'win', 'balance': 0}, {'result': 'lose', 'balance': 0}]),
    ({'win': 500, 'lose': 100}, [{'result': 'win', 'balance': 500}, {'result': 'lose', 'balance': -100}]),
    ({'win': 75, 'lose': 25}, [{'result': 'win', 'balance': 75}, {'result': 'lose', 'balance': -25}]),
])
def test_play_game_of_chance(strategy, expected_outcomes):
    result = play_game_of_chance(strategy)
    assert result in expected_outcomes
