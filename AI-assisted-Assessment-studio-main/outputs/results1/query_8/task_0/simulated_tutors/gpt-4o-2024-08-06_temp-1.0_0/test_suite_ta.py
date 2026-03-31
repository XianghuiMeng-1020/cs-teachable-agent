from program import *
import pytest
from program import identify_god

def test_war_god():
    result = identify_god('war')
    assert result == 'Ares'

def test_thunder_god():
    result = identify_god('thunder')
    assert result == 'Zeus'

def test_unknown_god():
    result = identify_god('water')
    assert result == 'Unknown'

def test_wisdom_god():
    result = identify_god('wisdom')
    assert result == 'Athena'

def test_underworld_god():
    result = identify_god('underworld')
    assert result == 'Hades'
