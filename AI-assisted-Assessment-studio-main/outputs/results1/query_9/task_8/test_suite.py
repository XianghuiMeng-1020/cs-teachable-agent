import pytest

@pytest.fixture()
def deities_list():
    return [
        {'name': 'Zeus', 'domain': 'sky', 'strength': 100},
        {'name': 'Hera', 'domain': 'family', 'strength': 80},
        {'name': 'Poseidon', 'domain': 'sea', 'strength': 90},
        {'name': 'Athena', 'domain': 'wisdom', 'strength': 85},
        {'name': 'Ares', 'domain': 'war', 'strength': 75},
    ]

@pytest.mark.parametrize("criteria, expected", [
    ({}, ['Zeus', 'Hera', 'Poseidon', 'Athena', 'Ares']),
    ({'min_strength': 85}, ['Zeus', 'Poseidon', 'Athena']),
    ({'domain': 'sea'}, ['Poseidon']),
    ({'min_strength': 80, 'domain': 'wisdom'}, ['Athena']),
    ({'min_strength': 95}, []),
    ({'domain': 'underworld'}, []),
])
def test_filter_deities(deities_list, criteria, expected):
    from solution_program import filter_deities
    assert filter_deities(deities_list, criteria) == expected