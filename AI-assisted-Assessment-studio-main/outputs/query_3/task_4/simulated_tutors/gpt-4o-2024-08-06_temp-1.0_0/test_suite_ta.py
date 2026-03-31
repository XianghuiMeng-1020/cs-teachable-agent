from program import *
import pytest

from program import classify_planets

def test_habitable_planet():
    result = classify_planets([
        {'name': 'Zorgon', 'atmos_density': 2.5, 'alien_life': True},
    ])
    assert result['Habitable'] == ['Zorgon']
    assert result['Potentially Habitable'] == []
    assert result['Uninhabitable'] == []

def test_potentially_habitable_planet():
    result = classify_planets([
        {'name': 'Lorca', 'atmos_density': 2.0, 'alien_life': False},
    ])
    assert result['Potentially Habitable'] == ['Lorca']
    assert result['Habitable'] == []
    assert result['Uninhabitable'] == []

def test_uninhabitable_planet_high_density():
    result = classify_planets([
        {'name': 'Arion', 'atmos_density': 3.1, 'alien_life': False},
    ])
    assert result['Uninhabitable'] == ['Arion']
    assert result['Potentially Habitable'] == []
    assert result['Habitable'] == []

def test_uninhabitable_planet_low_density():
    result = classify_planets([
        {'name': 'Blip', 'atmos_density': 0.9, 'alien_life': True},
    ])
    assert result['Uninhabitable'] == ['Blip']
    assert result['Potentially Habitable'] == []
    assert result['Habitable'] == []

def test_multiple_planet_classification():
    result = classify_planets([
        {'name': 'Zadok', 'atmos_density': 2.6, 'alien_life': True},
        {'name': 'Blorp', 'atmos_density': 1.5, 'alien_life': False},
        {'name': 'Sulek', 'atmos_density': 3.5, 'alien_life': False},
    ])
    assert result['Habitable'] == ['Zadok']
    assert result['Potentially Habitable'] == ['Blorp']
    assert result['Uninhabitable'] == ['Sulek']
