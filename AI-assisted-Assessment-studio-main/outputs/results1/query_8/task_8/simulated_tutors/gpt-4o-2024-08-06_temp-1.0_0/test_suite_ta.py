from program import *
import pytest

from program import classify_hero

@pytest.mark.parametrize("traits,expected", [
    ({'strength': 55, 'wisdom': 30, 'courage': 40}, 'Warrior'),
    ({'strength': 20, 'wisdom': 55, 'courage': 45}, 'Seer'),
    ({'strength': 40, 'wisdom': 40, 'courage': 55}, 'Champion'),
    ({'strength': 45, 'wisdom': 40, 'courage': 30}, 'Unsung Hero'),
    ({'strength': 50, 'wisdom': 50, 'courage': 50}, 'Unsung Hero'),
    ({'strength': 51, 'wisdom': 51, 'courage': 51}, 'Warrior'), # All traits are the same but 'strength' is highest with required threshold
    ({'strength': 49, 'wisdom': 50, 'courage': 51}, 'Champion'),
    ({'strength': 60, 'wisdom': 70, 'courage': 50}, 'Seer')
])
def test_classify_hero(traits, expected):
    assert classify_hero(traits) == expected
