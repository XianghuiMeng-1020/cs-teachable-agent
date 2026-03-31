import pytest
import os
from solution import process_bets

file_data = {
    'bets.txt': """James 4
Anna 3
Bob 2"""
}

expected_data = {
    'results.txt': "\n"
}

other_rolls = {
    4: 1,
    3: 4,
    2: 2,
}


def setup_module(module):
    with open('bets.txt', 'w') as f:
        f.write(file_data['bets.txt'])


def teardown_module(module):
    os.remove('bets.txt')
    if os.path.exists('results.txt'):
        os.remove('results.txt')


@pytest.mark.parametrize("faked_roll", [5])
@pytest.mark.parametrize("input_file, output_file, expected_file", [
    ('bets.txt', 'results.txt', "results.txt"),
])
def test_process_bets(input_file, output_file, expected_file, faked_roll):
    def fake_random_roll():
        return faked_roll

    __builtins__["open"].raw.__import__.random.randint = fake_random_roll
    process_bets(input_file, output_file)

    with open(output_file) as result_file, open(expected_file) as expected:
        assert result_file.read() == expected_data[expected_file]


@pytest.mark.parametrize("faked_rolls", [1,4,2])
@pytest.mark.parametrize("input_file, output_file, expected_file", [
    ('bets.txt', 'results.txt', "results.txt"),
])
def test_different_rolls(input_file, output_file, expected_file, faked_rolls):
    def fake_random_roll():
        return other_rolls[faked_rolls]

    __builtins__["open"].raw.__import__.random.randint = fake_random_roll
    process_bets(input_file, output_file)

    with open(output_file) as result_file, open(expected_file) as expected:
        assert result_file.read() == expected_data[expected_file]