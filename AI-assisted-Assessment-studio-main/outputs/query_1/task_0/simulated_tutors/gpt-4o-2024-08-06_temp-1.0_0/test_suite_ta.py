from program import *
import pytest

# Test Suite

def test_wielder_with_multiple_characters():
    artifacts = [('Mjölnir', 90), ('Excalibur', 75), ('Trident', 85)]
    power_requirements = [80, 95, 70, 100]
    assert determine_wielder_power(artifacts, power_requirements) == 3

def test_no_character_powerful_enough():
    artifacts = [('Gauntlet', 100), ('Golden Fleece', 150)]
    power_requirements = [50, 90]
    assert determine_wielder_power(artifacts, power_requirements) == 0

def test_single_artifact_sufficient_power():
    artifacts = [('Charon's Oar', 20)]
    power_requirements = [25]
    assert determine_wielder_power(artifacts, power_requirements) == 1

def test_exact_power_match():
    artifacts = [('Aegis Shield', 75)]
    power_requirements = [50, 75, 60]
    assert determine_wielder_power(artifacts, power_requirements) == 1

def test_empty_artifacts_list():
    artifacts = []
    power_requirements = [10, 20, 30]
    assert determine_wielder_power(artifacts, power_requirements) == 0
