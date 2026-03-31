from program import *
import pytest

from program import spin_wheel


def test_no_wins():
    bets = [(5, 10), (12, 20), (18, 5)]
    target = 7
    assert spin_wheel(bets, target) == 0


def test_single_bet_single_win():
    bets = [(24, 15)]
    target = 24
    assert spin_wheel(bets, target) == 150


def test_multiple_bets_single_win():
    bets = [(2, 100), (35, 50), (10, 25)]
    target = 35
    assert spin_wheel(bets, target) == 500


def test_multiple_bets_multiple_wins():
    bets = [(7, 30), (7, 50), (13, 20)]
    target = 7
    assert spin_wheel(bets, target) == 800


def test_high_stakes():
    bets = [(0, 200), (36, 10), (15, 100), (36, 90)]
    target = 36
    assert spin_wheel(bets, target) == 1000
