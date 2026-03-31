import pytest
from solution import decode_message

def test_decode_message_basic():
    codebook = {'QXZ':'hello', 'BFO':'world', 'DZT':'alien'}
    galactic_message = 'QXZ BFO GAO'
    assert decode_message(galactic_message, codebook) == 'hello world UNKNOWN'


def test_decode_message_full_match():
    codebook = {'AAA':'start', 'BBB':'middle', 'CCC':'end'}
    galactic_message = 'AAA BBB CCC'
    assert decode_message(galactic_message, codebook) == 'start middle end'


def test_decode_message_no_match():
    codebook = {'X':'one', 'Y':'two', 'Z':'three'}
    galactic_message = 'AAA BBB CCC'
    assert decode_message(galactic_message, codebook) == 'UNKNOWN UNKNOWN UNKNOWN'


def test_decode_message_empty_message():
    codebook = {'X':'yes', 'Y':'no'}
    galactic_message = ''
    assert decode_message(galactic_message, codebook) == ''


def test_decode_message_mixed_case():
    codebook = {'FOO':'foo', 'BAZ':'baz'}
    galactic_message = 'FOO BAR BAZ QUUX'
    assert decode_message(galactic_message, codebook) == 'foo UNKNOWN baz UNKNOWN'
