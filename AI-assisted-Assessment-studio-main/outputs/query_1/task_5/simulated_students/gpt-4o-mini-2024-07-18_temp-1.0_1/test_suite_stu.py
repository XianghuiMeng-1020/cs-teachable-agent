from solution_program import *
import pytest


def test_hydra_heads_basic():
    from solution_program import hydra_heads
    result = hydra_heads([4], [2])
    assert result == [8]


def test_hydra_heads_single_no_cuts():
    from solution_program import hydra_heads
    result = hydra_heads([3], [0])
    assert result == [3]


def test_hydra_heads_multiple_hydras():
    from solution_program import hydra_heads
    result = hydra_heads([10, 6], [3, 2])
    assert result == [16, 8]


def test_hydra_heads_large_heads_list():
    from solution_program import hydra_heads
    result = hydra_heads([20, 15, 10], [5, 2, 8])
    assert result == [30, 19, 14]


def test_hydra_heads_no_heads_case():
    from solution_program import hydra_heads
    result = hydra_heads([0], [3])
    assert result == [6]
