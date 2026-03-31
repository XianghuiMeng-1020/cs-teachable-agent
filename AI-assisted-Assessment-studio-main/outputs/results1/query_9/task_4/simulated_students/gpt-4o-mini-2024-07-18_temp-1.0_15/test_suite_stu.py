from solution_program import *
import pytest

# Test function to validate the functionality of pantheon_summary

def test_single_pantheon_multiple_gods():
    gods_list = [
        {'name': 'Odin', 'pantheon': 'Norse', 'realm': 'Wisdom'},
        {'name': 'Thor', 'pantheon': 'Norse', 'realm': 'Thunder'},
        {'name': 'Freyja', 'pantheon': 'Norse', 'realm': 'Love'}
    ]
    assert pantheon_summary(gods_list) == {
        'Norse': {'count': 3, 'realms': ['Love', 'Thunder', 'Wisdom']}
    }

def test_multiple_pantheons():
    gods_list = [
        {'name': 'Zeus', 'pantheon': 'Greek', 'realm': 'Sky'},
        {'name': 'Hera', 'pantheon': 'Greek', 'realm': 'Marriage'},
        {'name': 'Odin', 'pantheon': 'Norse', 'realm': 'Wisdom'},
        {'name': 'Freyr', 'pantheon': 'Norse', 'realm': 'Prosperity'}
    ]
    assert pantheon_summary(gods_list) == {
        'Greek': {'count': 2, 'realms': ['Marriage', 'Sky']},
        'Norse': {'count': 2, 'realms': ['Prosperity', 'Wisdom']}
    }

def test_no_gods():
    gods_list = []
    assert pantheon_summary(gods_list) == {}

def test_single_god():
    gods_list = [
        {'name': 'Ra', 'pantheon': 'Egyptian', 'realm': 'Sun'}
    ]
    assert pantheon_summary(gods_list) == {
        'Egyptian': {'count': 1, 'realms': ['Sun']}
    }

def test_multiple_gods_same_realm():
    gods_list = [
        {'name': 'Ra', 'pantheon': 'Egyptian', 'realm': 'Sun'},
        {'name': 'Anubis', 'pantheon': 'Egyptian', 'realm': 'Afterlife'},
        {'name': 'Isis', 'pantheon': 'Egyptian', 'realm': 'Magic'},
        {'name': 'Osiris', 'pantheon': 'Egyptian', 'realm': 'Afterlife'}
    ]
    assert pantheon_summary(gods_list) == {
        'Egyptian': {'count': 4, 'realms': ['Afterlife', 'Magic', 'Sun']}
    }
