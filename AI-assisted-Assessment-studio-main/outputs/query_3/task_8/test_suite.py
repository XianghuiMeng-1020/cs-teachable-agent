
import pytest
from solution import decrypt_message

# Sample Data for Testing
# Definition of galactic cipher and protocols for testing
setup_complete = False
galactic_cipher = {}
galactic_protocols = {}

def setup_module(module):
    global setup_complete, galactic_cipher, galactic_protocols
    if not setup_complete:
        galactic_cipher = {
            'A': 'Z',
            'B': 'Y',
            'C': 'X',
            'D': 'W',
            'E': 'V',
            'F': 'U',
            '1': '9'
        }

        galactic_protocols = {
            'FOO': 'HELLO',
            'BAR': 'WORLD',
            '123': 'SPACE'
        }
        setup_complete = True

def teardown_module(module):
    global setup_complete, galactic_cipher, galactic_protocols
    setup_complete = False
    galactic_cipher.clear()
    galactic_protocols.clear()

# Sample Test Cases

def test_single_protocol_match():
    assert decrypt_message("FOO") == "HELLO"


def test_mixed_protocol_and_character_decryption():
    assert decrypt_message("FOOBAR123") == "HELLOWORLDSPACE"


def test_individual_character_decryption():
    assert decrypt_message("C1F") == "X9U"


def test_no_matching_protocols():
    assert decrypt_message("ACF") == "ZXU"


def test_message_with_all_protocols_and_chars():
    assert decrypt_message("FOO123A1C") == "HELLOSPACEZ9X"
