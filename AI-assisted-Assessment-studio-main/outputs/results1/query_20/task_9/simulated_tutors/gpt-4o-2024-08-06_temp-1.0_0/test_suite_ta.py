from program import *
import pytest
from program import calculate_score

def test_full_development():
    assert calculate_score("AAA", "AAA") == 24

def test_partial_development():
    assert calculate_score("ABC", "AB") == 21

def test_no_development():
    assert calculate_score("XYZ", "") == 15

def test_mixed_development():
    assert calculate_score("MNPQ", "PQ") == 18

def test_empty_controlled():
    assert calculate_score("", "" ) == 0