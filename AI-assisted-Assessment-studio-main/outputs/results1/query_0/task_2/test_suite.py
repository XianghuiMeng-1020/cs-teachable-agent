import pytest
import os
from solution import game_of_chance

def setup_module(module):
    with open('test_lottery_tickets.txt', 'w') as file:
        file.write('1234\n')
        file.write('5678\n')
        file.write('91011\n')
        file.write('11213\n')

def teardown_module(module):
    os.remove('test_lottery_tickets.txt')

def test_ticket_match_and_lengths_equal():
    assert game_of_chance('test_lottery_tickets.txt', '1234', '5678') == "WIN"

def test_ticket_match_and_ticket_longer():
    assert game_of_chance('test_lottery_tickets.txt', '91011', '123') == "JACKPOT"

def test_ticket_not_found():
    assert game_of_chance('test_lottery_tickets.txt', '0000', '5678') == "TICKET NOT FOUND"

def test_ticket_match_and_draw_longer():
    assert game_of_chance('test_lottery_tickets.txt', '5678', '123456') == "NO WIN"

def test_another_ticket_match_and_ticket_longer():
    assert game_of_chance('test_lottery_tickets.txt', '11213', '1234') == "JACKPOT"
