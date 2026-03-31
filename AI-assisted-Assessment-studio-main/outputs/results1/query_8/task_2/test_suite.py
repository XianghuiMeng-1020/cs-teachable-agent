import pytest
from solution import classify_creature

def test_sky_creatures():
    assert classify_creature('Phoenix') == 'sky'
    assert classify_creature('Garuda') == 'sky'
    assert classify_creature('Thunderbird') == 'sky'

def test_sea_creatures():
    assert classify_creature('Kraken') == 'sea'
    assert classify_creature('Leviathan') == 'sea'
    assert classify_creature('Mermaid') == 'sea'

def test_earth_creatures():
    assert classify_creature('Golem') == 'earth'
    assert classify_creature('Satyr') == 'earth'
    assert classify_creature('Nymph') == 'earth'

def test_other_creatures():
    assert classify_creature('Goblin') == 'other'
    assert classify_creature('Unicorn') == 'other'
    assert classify_creature('Dragon') == 'other'

def test_edge_cases():
    assert classify_creature('') == 'other'
    assert classify_creature('Pixie') == 'other'
