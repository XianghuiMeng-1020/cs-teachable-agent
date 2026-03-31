from program import *
import pytest

from program import calculate_winnings

@pytest.mark.parametrize("tosses, expected", [
    ("HTHTTHH", 5),
    ("HHH", 6),
    ("TTTTT", -5),
    ("THTHTH", -1),
    ("HTHHTTT", 1),
    ("", 0),
    ("HTHTHTHTHTHTHTHTHTHT", -2),
    ("HHHTTT", 0),
    ("HHTHHTTTT", 0),
    ("T" * 1000, -1000)
])
def test_calculate_winnings(tosses, expected):
    assert calculate_winnings(tosses) == expected