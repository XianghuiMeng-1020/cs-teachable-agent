import pytest

@pytest.fixture(scope="module")
def creature_data_set_1():
    return {
        'Phoenix': 'Fire',
        'Kraken': 'Ocean',
        'Dragon': 'Fire',
        'Nymph': 'Forest',
        'Mermaid': 'Ocean'
    }

@pytest.fixture(scope="module")
def creature_data_set_2():
    return {
        'Centaur': 'Forest',
        'Ice Giant': 'Ice',
        'Firebird': 'Fire',
        'Leviathan': 'Ocean'
    }

@pytest.fixture(scope="module")
def creature_data_set_3():
    return {
        'Cyclops': 'Cave',
        'Minotaur': 'Labyrinth',
        'Pegasus': 'Sky'
    }

@pytest.fixture(scope="module")
def creature_data_empty():
    return {}

@pytest.fixture(scope="module")
def creature_data_single():
    return {
        'Unicorn': 'Forest'
    }

from solution import sort_creatures_by_realm

def test_sort_creatures_by_realm_base_case(creature_data_set_1):
    result = sort_creatures_by_realm(creature_data_set_1)
    assert result == {
        'Fire': ['Dragon', 'Phoenix'],
        'Ocean': ['Kraken', 'Mermaid'],
        'Forest': ['Nymph']
    }


def test_sort_creatures_by_realm_varied_realms(creature_data_set_2):
    result = sort_creatures_by_realm(creature_data_set_2)
    assert result == {
        'Fire': ['Firebird'],
        'Ocean': ['Leviathan'],
        'Forest': ['Centaur'],
        'Ice': ['Ice Giant']
    }


def test_sort_creatures_by_realm_unique_realms(creature_data_set_3):
    result = sort_creatures_by_realm(creature_data_set_3)
    assert result == {
        'Cave': ['Cyclops'],
        'Labyrinth': ['Minotaur'],
        'Sky': ['Pegasus']
    }


def test_sort_creatures_by_realm_empty(creature_data_empty):
    result = sort_creatures_by_realm(creature_data_empty)
    assert result == {}


def test_sort_creatures_by_realm_single_creature(creature_data_single):
    result = sort_creatures_by_realm(creature_data_single)
    assert result == {
        'Forest': ['Unicorn']
    }
