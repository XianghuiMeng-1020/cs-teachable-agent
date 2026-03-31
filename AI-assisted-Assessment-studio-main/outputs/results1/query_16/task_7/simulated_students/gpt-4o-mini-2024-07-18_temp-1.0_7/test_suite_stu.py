from solution_program import *
import pytest
from solution_program import InterstellarMessage

@pytest.fixture
def setup_module():
    pass

@pytest.fixture
def teardown_module():
    pass

class TestInterstellarMessage:
    def test_encode_simple_message(self):
        msg = InterstellarMessage("HELLO", 3)
        assert msg.encode() == "KHOOR"

    def test_decode_simple_message(self):
        msg = InterstellarMessage("HELLO", 3)
        encoded = msg.encode()
        assert msg.decode(encoded) == "HELLO"

    def test_encode_with_special_characters(self):
        msg = InterstellarMessage("GREETINGS!", 4)
        assert msg.encode() == "KVIIZMKSR!"

    def test_decode_with_special_characters(self):
        msg = InterstellarMessage("GREETINGS!", 4)
        encoded = msg.encode()
        assert msg.decode(encoded) == "GREETINGS!"

    def test_non_printable_characters_exception(self):
        with pytest.raises(ValueError):
            msg = InterstellarMessage("HELLO", 100)
            msg.encode()