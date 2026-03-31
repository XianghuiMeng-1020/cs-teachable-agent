from program import *
import pytest
from program import god_info

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_known_god1():
    assert god_info("Zeus") == "Domain: Sky and Thunder, Symbol: Thunderbolt"


def test_known_god2():
    assert god_info("poseidon") == "Domain: Sea, Symbol: Trident"


def test_known_god3():
    assert god_info("ARes") == "Domain: War, Symbol: Spear"


def test_known_god4():
    assert god_info("Aphrodite") == "Domain: Love, Symbol: Dove"


def test_unknown_god1():
    assert god_info("Hera") == "Unknown god"


def test_unknown_god2():
    assert god_info("Thor") == "Unknown god"


def test_case_sensitivity1():
    assert god_info("athena") == "Domain: Wisdom, Symbol: Owl"


def test_case_sensitivity2():
    assert god_info("ADES") == "Domain: Underworld, Symbol: Helmet of invisibility"

