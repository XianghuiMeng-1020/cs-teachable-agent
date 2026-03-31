import pytest
import os
from solution import lucky_numbers

players_content = '''John,25\nAlice,5\nBob,15\nSue,10\n'''
winning_content = '5,10,25,40'
expected_results_1 = '''John: 1\nAlice: 1\nBob: 1\nSue: 1\n'''

players_empty = ''
winning_empty = ''
expected_results_2 = ''

players_no_match = '''Anna,3\nMike,11\nSam,20\n'''
winning_no_match = '99,100,101'
expected_results_3 = '''Anna: 0\nMike: 0\nSam: 0\n'''

@pytest.fixture(autouse=True)
def setup_module():
    with open('players.txt', 'w') as f:
        f.write(players_content)
    with open('winning_numbers.txt', 'w') as f:
        f.write(winning_content)
    yield
    teardown_module()

@pytest.fixture()
def teardown_module():
    os.remove('players.txt')
    os.remove('winning_numbers.txt')
    if os.path.exists('results.txt'):
        os.remove('results.txt')

# Base case
@pytest.mark.parametrize("players, winnings, expected_results", [
    (players_content, winning_content, expected_results_1)
])
def test_lucky_numbers_base(players, winnings, expected_results):
    with open('players.txt', 'w') as f:
        f.write(players)
    with open('winning_numbers.txt', 'w') as f:
        f.write(winnings)

    lucky_numbers()

    with open('results.txt', 'r') as result_file:
        results = result_file.read()
    assert results == expected_results

# Edge cases
@pytest.mark.parametrize("players, winnings, expected_results", [
    (players_empty, winning_empty, expected_results_2),
    (players_no_match, winning_no_match, expected_results_3)
])
def test_lucky_numbers_edges(players, winnings, expected_results):
    with open('players.txt', 'w') as f:
        f.write(players)
    with open('winning_numbers.txt', 'w') as f:
        f.write(winnings)

    lucky_numbers()

    with open('results.txt', 'r') as result_file:
        results = result_file.read()
    assert results == expected_results