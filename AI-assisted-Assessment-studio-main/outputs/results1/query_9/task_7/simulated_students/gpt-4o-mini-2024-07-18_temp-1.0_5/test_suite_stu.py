from solution_program import *
import pytest

from solution_program import group_by_domain

def test_group_by_domain():
    characters = [
        ['Zeus', 'Sky'],
        ['Poseidon', 'Sea'],
        ['Hades', 'Underworld'],
        ['Hera', 'Marriage'],
        ['Aphrodite', 'Love'],
        ['Ares', 'War'],
        ['Athena', 'Wisdom'],
        ['Hephaestus', 'Forge'],
        ['Demeter', 'Harvest'],
        ['Dionysus', 'Wine'],
        ['Hermes', 'Travel'],
        ['Artemis', 'Hunt'],
        ['Apollo', 'Sun'],
        ['Nyx', 'Night']
    ]
    expected_output = {
        'Sky': ['Zeus'],
        'Sea': ['Poseidon'],
        'Underworld': ['Hades'],
        'Marriage': ['Hera'],
        'Love': ['Aphrodite'],
        'War': ['Ares'],
        'Wisdom': ['Athena'],
        'Forge': ['Hephaestus'],
        'Harvest': ['Demeter'],
        'Wine': ['Dionysus'],
        'Travel': ['Hermes'],
        'Hunt': ['Artemis'],
        'Sun': ['Apollo'],
        'Night': ['Nyx']
    }
    assert group_by_domain(characters) == expected_output

    characters = [
        ['Thor', 'Thunder'],
        ['Odin', 'Wisdom'],
        ['Loki', 'Trickery'],
        ['Freya', 'Love'],
        ['Frigg', 'Marriage'],
        ['Balder', 'Light'],
        ['Hel', 'Underworld'],
        ['Frey', 'Fertility'],
    ]
    expected_output = {
        'Thunder': ['Thor'],
        'Wisdom': ['Odin'],
        'Trickery': ['Loki'],
        'Love': ['Freya'],
        'Marriage': ['Frigg'],
        'Light': ['Balder'],
        'Underworld': ['Hel'],
        'Fertility': ['Frey'],
    }
    assert group_by_domain(characters) == expected_output

    characters = [
        ['Anubis', 'Afterlife'],
        ['Ra', 'Sun'],
        ['Osiris', 'Resurrection'],
        ['Horus', 'Sky'],
        ['Isis', 'Magic'],
        ['Thoth', 'Wisdom'],
        ['Set', 'Chaos'],
        ['Bastet', 'Home'],
    ]
    expected_output = {
        'Afterlife': ['Anubis'],
        'Sun': ['Ra'],
        'Resurrection': ['Osiris'],
        'Sky': ['Horus'],
        'Magic': ['Isis'],
        'Wisdom': ['Thoth'],
        'Chaos': ['Set'],
        'Home': ['Bastet'],
    }
    assert group_by_domain(characters) == expected_output

    characters = []
    expected_output = {}
    assert group_by_domain(characters) == expected_output

    characters = [
        ['Zeus', 'Sky'],
        ['Hera', 'Marriage'],
        ['Thor', 'Sky']
    ]
    expected_output = {
        'Sky': ['Zeus', 'Thor'],
        'Marriage': ['Hera']
    }
    assert group_by_domain(characters) == expected_output
