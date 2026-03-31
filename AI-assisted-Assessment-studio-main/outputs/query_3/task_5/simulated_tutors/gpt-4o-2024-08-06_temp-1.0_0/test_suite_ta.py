from program import *
import pytest

from program import decode_message

def test_decode_message_case_1():
    code = "ABCAAA"
    translation_rules = {'A': 10, 'B': 5, 'C': 2}
    assert decode_message(code, translation_rules) == 39

def test_decode_message_case_2():
    code = "XXYYZ"
    translation_rules = {'X': 3, 'Y': 4}
    assert decode_message(code, translation_rules) == 14

def test_decode_message_case_3():
    code = ""
    translation_rules = {'A': 1}
    assert decode_message(code, translation_rules) == 0

def test_decode_message_case_4():
    code = "ZZZZ"
    translation_rules = {'Z': 0}
    assert decode_message(code, translation_rules) == 0

def test_decode_message_case_5():
    code = "PTQ"
    translation_rules = {}
    assert decode_message(code, translation_rules) == 0