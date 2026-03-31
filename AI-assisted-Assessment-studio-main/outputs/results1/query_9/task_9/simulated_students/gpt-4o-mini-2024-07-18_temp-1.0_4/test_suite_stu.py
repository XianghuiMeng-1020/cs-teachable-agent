from solution_program import *
import pytest

from solution_program import analyze_mythical_creatures

# Test Case 1: Basic functionality with mixed origins
creatures1 = [
    {'name': 'Cerberus', 'story_count': 3, 'origin': 'Greek'},
    {'name': 'Fenrir', 'story_count': 2, 'origin': 'Norse'},
    {'name': 'Phoenix', 'story_count': 4, 'origin': 'Greek'},
    {'name': 'Jormungandr', 'story_count': 1, 'origin': 'Norse'},
]
expected1 = {
    'total_stories': 10,
    'creature_count': {'Cerberus': 3, 'Fenrir': 2, 'Phoenix': 4, 'Jormungandr': 1},
    'origin_count': {'Greek': 7, 'Norse': 3}
}

def test_analyze_mythical_creatures_case1():
    assert analyze_mythical_creatures(creatures1) == expected1

# Test Case 2: All creatures from the same origin
creatures2 = [
    {'name': 'Medusa', 'story_count': 5, 'origin': 'Greek'},
    {'name': 'Minotaur', 'story_count': 2, 'origin': 'Greek'},
]
expected2 = {
    'total_stories': 7,
    'creature_count': {'Medusa': 5, 'Minotaur': 2},
    'origin_count': {'Greek': 7}
}

def test_analyze_mythical_creatures_case2():
    assert analyze_mythical_creatures(creatures2) == expected2

# Test Case 3: Single creature with multiple stories
creatures3 = [
    {'name': 'Dragon', 'story_count': 10, 'origin': 'Chinese'},
]
expected3 = {
    'total_stories': 10,
    'creature_count': {'Dragon': 10},
    'origin_count': {'Chinese': 10}
}

def test_analyze_mythical_creatures_case3():
    assert analyze_mythical_creatures(creatures3) == expected3

# Test Case 4: Empty list of creatures
creatures4 = []
expected4 = {
    'total_stories': 0,
    'creature_count': {},
    'origin_count': {}
}

def test_analyze_mythical_creatures_case4():
    assert analyze_mythical_creatures(creatures4) == expected4

# Test Case 5: Testing single story with unique name
creatures5 = [
    {'name': 'Kraken', 'story_count': 1, 'origin': 'Nordic'},
]
expected5 = {
    'total_stories': 1,
    'creature_count': {'Kraken': 1},
    'origin_count': {'Nordic': 1}
}

def test_analyze_mythical_creatures_case5():
    assert analyze_mythical_creatures(creatures5) == expected5
