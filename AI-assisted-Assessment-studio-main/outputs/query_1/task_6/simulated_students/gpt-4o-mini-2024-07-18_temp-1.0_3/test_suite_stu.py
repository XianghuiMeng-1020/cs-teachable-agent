from solution_program import *
import pytest

from solution_program import calculate_mythical_power

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup before tests
    yield
    # Teardown after tests

# Test with all strong affinities
@pytest.mark.parametrize("affinities, expected", [
    ([15, 20, 25], 2*15 + 2*20 + 2*25),
    ([11, 12], 2*11 + 2*12)])
def test_all_strong_affinities(calculate_mythical_power, affinities, expected):
    assert calculate_mythical_power(affinities) == expected

# Test with all moderate affinities
@pytest.mark.parametrize("affinities, expected", [
    ([5, 6, 10], 5 + 6 + 10),
    ([7], 7)])
def test_all_moderate_affinities(calculate_mythical_power, affinities, expected):
    assert calculate_mythical_power(affinities) == expected

# Test with all weak affinities
@pytest.mark.parametrize("affinities, expected", [
    ([1, 2, 3], -(2*1 + 2*2 + 2*3)),
    ([4], -(2*4))])
def test_all_weak_affinities(calculate_mythical_power, affinities, expected):
    assert calculate_mythical_power(affinities) == expected

# Test with a mix of affinities
@pytest.mark.parametrize("affinities, expected", [
    ([3, 5, 11], -(2*3) + 5 + 2*11),
    ([15, 7, 2], 2*15 + 7 - (2*2))])
def test_mixed_affinities(calculate_mythical_power, affinities, expected):
    assert calculate_mythical_power(affinities) == expected

# Test with an empty list
@pytest.mark.parametrize("affinities, expected", [
    ([], 0)])
def test_empty_affinities(calculate_mythical_power, affinities, expected):
    assert calculate_mythical_power(affinities) == expected
