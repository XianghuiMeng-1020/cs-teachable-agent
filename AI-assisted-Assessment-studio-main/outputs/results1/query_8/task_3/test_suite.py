import pytest

from solution import assign_mythological_creature

def test_known_signs():
    assert assign_mythological_creature('Aries') == 'Dragon'
    assert assign_mythological_creature('Taurus') == 'Minotaur'
    assert assign_mythological_creature('Gemini') == 'Griffin'
    assert assign_mythological_creature('Cancer') == 'Cyclops'
    assert assign_mythological_creature('Leo') == 'Phoenix'
    assert assign_mythological_creature('Virgo') == 'Sphinx'
    assert assign_mythological_creature('Libra') == 'Centaur'
    assert assign_mythological_creature('Scorpio') == 'Hydra'
    assert assign_mythological_creature('Sagittarius') == 'Pegasus'
    assert assign_mythological_creature('Capricorn') == 'Leviathan'
    assert assign_mythological_creature('Aquarius') == 'Kraken'
    assert assign_mythological_creature('Pisces') == 'Mermaid'

def test_unknown_sign():
    assert assign_mythological_creature('Ophiuchus') == 'Unknown Creature'

def test_empty_string():
    assert assign_mythological_creature('') == 'Unknown Creature'

def test_lowercase_sign():
    assert assign_mythological_creature('aries') == 'Unknown Creature'

def test_random_string():
    assert assign_mythological_creature('NotAZodiac') == 'Unknown Creature'
