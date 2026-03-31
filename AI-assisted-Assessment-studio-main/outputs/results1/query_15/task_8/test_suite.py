import pytest

from solution_program import encode_message

@pytest.mark.parametrize("message, expected", [
    ("hello world", "hillu wurld"),
    ("space voyage", "spici vuyegi"),
    ("science fiction", "sciinci ficoiun"),
    ("universes collide", "anovirsis celluldi"),
    ("aeiou", "eioua"),
    ("cryptography", "cryptugrephy"),
    ("all vowels", "ell vuwils"),
    ("aaaaa", "eeeee"),
    ("r q u", "r q a"),
    ("xylophones and zithers", "xuluiphunis end zuthirs"),
    ("", "")  # Test for an empty string
])
def test_encode_message(message, expected):
    assert encode_message(message) == expected