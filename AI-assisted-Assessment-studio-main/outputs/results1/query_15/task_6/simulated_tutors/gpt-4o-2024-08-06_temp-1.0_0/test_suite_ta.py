from program import *
import pytest
from program import decode_alien_message

@pytest.mark.parametrize("message, expected", [
    ("abc", [1, 2, 3]),
    ("zzz", [26, 26, 26]),
    ("hello", [8, 5, 12, 12, 15]),
    ("sphinx", [19, 16, 8, 9, 14, 24]),
    ("space", [19, 16, 1, 3, 5]),
    ("quantum", [17, 21, 1, 14, 20, 21, 13]),
    ("python", [16, 25, 20, 8, 15, 14]),
    ("a", [1]),
    ("zebra", [26, 5, 2, 18, 1]),
    ("moon", [13, 15, 15, 14])
])
def test_decode_alien_message(message, expected):
    assert decode_alien_message(message) == expected
