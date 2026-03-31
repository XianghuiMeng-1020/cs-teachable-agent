import pytest
from solution import describe_god

def setup_module(module):
    pass

def teardown_module(module):
    pass

def test_zeus():
    assert describe_god("Zeus") == "God of the sky and thunder"


def test_poseidon():
    assert describe_god("poseidon") == "God of the sea"


def test_unknown_god():
    assert describe_god("Hermes") == "Unknown god"


def test_athena_mixed_case():
    assert describe_god("aThEnA") == "Goddess of wisdom and war"


def test_hades_lowercase():
    assert describe_god("hades") == "God of the underworld"
