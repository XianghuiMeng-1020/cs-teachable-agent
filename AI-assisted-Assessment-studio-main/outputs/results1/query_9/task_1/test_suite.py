import pytest

from solution import count_gods_attributes

def test_example_case():
    gods_list = [
        {"name": "zeus", "attributes": ["thunder", "sky", "justice"]},
        {"name": "hera", "attributes": ["marriage", "sky", "womanhood"]},
        {"name": "poseidon", "attributes": ["sea", "horses", "earthquake"]},
        {"name": "athena", "attributes": ["wisdom", "war", "justice"]},
    ]
    expected = {
        "thunder": 1,
        "sky": 2,
        "justice": 2,
        "marriage": 1,
        "womanhood": 1,
        "sea": 1,
        "horses": 1,
        "earthquake": 1,
        "wisdom": 1,
        "war": 1
    }
    assert count_gods_attributes(gods_list) == expected


def test_single_god_single_attribute():
    gods_list = [
        {"name": "apollo", "attributes": ["sun"]}
    ]
    expected = {"sun": 1}
    assert count_gods_attributes(gods_list) == expected


def test_single_god_multiple_attributes():
    gods_list = [
        {"name": "ares", "attributes": ["war", "violence"]}
    ]
    expected = {"war": 1, "violence": 1}
    assert count_gods_attributes(gods_list) == expected


def test_multiple_gods_same_attributes():
    gods_list = [
        {"name": "hephaestus", "attributes": ["fire", "craft"]},
        {"name": "hestia", "attributes": ["fire", "home"]}
    ]
    expected = {"fire": 2, "craft": 1, "home": 1}
    assert count_gods_attributes(gods_list) == expected


def test_no_duplicate_attributes_within_same_god():
    gods_list = [
        {"name": "hermes", "attributes": ["messenger", "travel", "travel"]}
    ]
    expected = {"messenger": 1, "travel": 2}
    assert count_gods_attributes(gods_list) == expected
