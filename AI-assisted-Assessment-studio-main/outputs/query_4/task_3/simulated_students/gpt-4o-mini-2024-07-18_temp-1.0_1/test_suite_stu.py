from solution_program import *
import pytest

from solution_program import calculate_player_scores

def test_base_case():
    players = ['Alice', 'Bob', 'Charlie']
    scores = [[10, 20, 30], [15, 25], [5, 10, 5, 10]]
    expected = {'Alice': 60, 'Bob': 40, 'Charlie': 30}
    assert calculate_player_scores(players, scores) == expected

def test_different_lengths():
    players = ['Dave', 'Ed']
    scores = [[5, 5, 5], [20, 20]]
    expected = {'Dave': 15, 'Ed': 40}
    assert calculate_player_scores(players, scores) == expected

def test_single_player():
    players = ['Frank']
    scores = [[100, -50, 50]]
    expected = {'Frank': 100}
    assert calculate_player_scores(players, scores) == expected

def test_no_scores():
    players = ['Grace', 'Hank']
    scores = [[], []]
    expected = {'Grace': 0, 'Hank': 0}
    assert calculate_player_scores(players, scores) == expected

def test_negative_scores():
    players = ['Ivy']
    scores = [[-20, -10, -5]]
    expected = {'Ivy': -35}
    assert calculate_player_scores(players, scores) == expected
