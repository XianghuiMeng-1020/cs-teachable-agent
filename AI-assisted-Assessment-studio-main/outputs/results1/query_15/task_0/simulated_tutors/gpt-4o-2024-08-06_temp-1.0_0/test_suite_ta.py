from program import *
import pytest
from program import can_teleport_sequence

def test_can_teleport_base_case():
    assert can_teleport_sequence([1, 2, 3], [(1, 2), (2, 3)]) == True

def test_cannot_teleport_out_of_order():
    assert can_teleport_sequence([1, 2, 3], [(1, 3), (3, 2)]) == False

def test_direct_teleport_only_last_fails():
    assert can_teleport_sequence([4, 5, 6], [(4, 5)]) == False

def test_simple_cyclic_connection_fails():
    assert can_teleport_sequence([2, 4, 5], [(2, 4), (4, 2)]) == False

def test_connection_does_not_start_properly():
    assert can_teleport_sequence([1, 4, 5], [(2, 4), (4, 5)]) == False
