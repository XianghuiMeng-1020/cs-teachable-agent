from program import *
import pytest

from program import translate_astronyms

def test_translate_known_astronyms():
    assert translate_astronyms(['xer', 'plethora', 'gicon'], {'xer': 'Star', 'plethora': 'Galaxy', 'gicon': 'Nebula'}) == ['Star', 'Galaxy', 'Nebula']

def test_translate_with_unknown_astronyms():
    assert translate_astronyms(['xer', 'unknown', 'gicon', 'zuru'], {'xer': 'Star', 'gicon': 'Nebula'}) == ['Star', 'Unknown', 'Nebula', 'Unknown']

def test_translate_no_matches():
    assert translate_astronyms(['alpha', 'beta', 'gamma'], {'xer': 'Star'}) == ['Unknown', 'Unknown', 'Unknown']

def test_translate_partial_matches():
    assert translate_astronyms(['orb', 'ether', 'neb'], {'orb': 'Planet', 'neb': 'Icefield'}) == ['Planet', 'Unknown', 'Icefield']

def test_translate_empty_dictionary():
    assert translate_astronyms(['xer', 'gicon'], {}) == ['Unknown', 'Unknown']
