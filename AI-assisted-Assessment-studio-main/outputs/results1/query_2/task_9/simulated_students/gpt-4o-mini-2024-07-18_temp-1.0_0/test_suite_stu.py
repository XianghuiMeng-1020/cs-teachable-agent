from solution_program import *
import pytest
import os
from solution_program import register_entries, draw_winner

@pytest.fixture(scope="module")
def setup_module():
    with open('test_lottery.txt', 'w') as f:
        f.write("Alice\nBob\n")
    yield
    os.remove('test_lottery.txt')

@pytest.mark.usefixtures("setup_module")
class TestLottery:
    def test_register_entries_appends(self):
        register_entries('test_lottery.txt', ['Charlie', 'Diana'])
        with open('test_lottery.txt', 'r') as f:
            lines = f.read().strip().split('\n')
        assert lines == ['Alice', 'Bob', 'Charlie', 'Diana']

    def test_draw_winner_with_entries(self):
        entries, winner = draw_winner('test_lottery.txt')
        assert len(entries) == 4
        assert winner in entries

    def test_draw_winner_no_entries(self):
        with open('empty_lottery.txt', 'w') as f:
            pass
        result = draw_winner('empty_lottery.txt')
        assert result == []
        os.remove('empty_lottery.txt')

    def test_register_entries_to_empty_file(self):
        with open('new_lottery.txt', 'w') as f:
            pass
        register_entries('new_lottery.txt', ['Eve', 'Frank'])
        with open('new_lottery.txt', 'r') as f:
            lines = f.read().strip().split('\n')
        assert lines == ['Eve', 'Frank']
        os.remove('new_lottery.txt')

    def test_draw_winner_single_entry(self):
        with open('single_lottery.txt', 'w') as f:
            f.write("Gina\n")
        entries, winner = draw_winner('single_lottery.txt')
        assert entries == ['Gina']
        assert winner == 'Gina'
        os.remove('single_lottery.txt')