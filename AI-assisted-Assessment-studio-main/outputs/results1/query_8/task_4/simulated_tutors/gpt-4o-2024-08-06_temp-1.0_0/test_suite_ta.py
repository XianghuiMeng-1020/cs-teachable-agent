from program import *
import pytest
from program import mythological_judgment

def test_zeus_help():
    result = mythological_judgment("zeus", "help")
    assert result == "Blessing granted"

def test_zeus_other_action():
    result = mythological_judgment("zeus", "fight")
    assert result == "Storms befall you"

def test_cerberus_steal():
    result = mythological_judgment("cerberus", "steal")
    assert result == "Growling disapproval"

def test_cerberus_other_action():
    result = mythological_judgment("cerberus", "explore")
    assert result == "Pass freely"

def test_aphrodite_love():
    result = mythological_judgment("aphrodite", "love")
    assert result == "Heart's desire fulfilled"

def test_other_creature():
    result = mythological_judgment("minotaur", "roar")
    assert result == "No judgment found"