from program import *
import pytest

from program import guard_treasure

@pytest.mark.parametrize("guards, expected", [
    ([('Athena', 1), ('Hermes', 2), ('Apollo', 3), ('Artemis', 4)], ['Athena', 'Apollo']),
    ([('Zeus', 7), ('Hera', 5)], ['Zeus', 'Hera']),
    ([('Poseidon', 2), ('Demeter', 8)], []),
    ([('Ares', 9), ('Athena', 13), ('Hephaestus', 18)], ['Ares', 'Athena']),
    ([('Hermes', 100)], [])
])
def test_guard_treasure(guards, expected):
    assert guard_treasure(guards) == expected