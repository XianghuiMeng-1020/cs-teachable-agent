from solution_program import *
import pytest
from solution_program import AlienRegistry

def test_add_and_get_species_info():
    registry = AlienRegistry()
    registry.add_species("Zog", {"color": "blue", "limbs": "tentacles"})
    info = registry.get_species_info("Zog")
    assert info == {"color": "blue", "limbs": "tentacles"}

    registry.add_species("Quo", {"color": "green", "limbs": "arms"})
    info = registry.get_species_info("Quo")
    assert info == {"color": "green", "limbs": "arms"}

    with pytest.raises(ValueError) as excinfo:
        registry.get_species_info("Nonexistent")
    assert str(excinfo.value) == "Species not found"


def test_get_all_species():
    registry = AlienRegistry()
    registry.add_species("Xenon", {"size": "large"})
    registry.add_species("Ael", {"size": "small"})
    registry.add_species("Zex", {"size": "medium"})
    species_list = registry.get_all_species()
    assert species_list == ["Ael", "Xenon", "Zex"]


def test_add_duplicate_species():
    registry = AlienRegistry()
    registry.add_species("Blor", {"color": "red"})
    registry.add_species("Blor", {"color": "green"})  # Attempt to add duplicate
    info = registry.get_species_info("Blor")
    assert info == {"color": "red"}  # Characteristics should not change


def test_handle_empty_registry():
    registry = AlienRegistry()
    with pytest.raises(ValueError) as excinfo:
        registry.get_species_info("Alpha")
    assert str(excinfo.value) == "Species not found"
    assert registry.get_all_species() == []