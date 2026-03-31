import pytest
import os
from solution import SciFiHaiku

def setup_module(module):
    with open('test_input.txt', 'w') as f:
        f.write('3+2_in_space 8-1_SN 2*2=5 where stars shine')

def teardown_module(module):
    os.remove('test_input.txt')

def test_sci_fi_haiku_import_input():
    with open('test_input.txt', 'r') as f:
        text = f.read()
    haiku = SciFiHaiku(text)
    result = haiku.generate_haiku()
    expected = ['3+2_', 'in_space', '8-1_', 'SN', '2x2=', 'Err', 'where', 'stars', 'shine']
    assert result == expected


def test_sci_fi_haiku_invalid_expression():
    haiku = SciFiHaiku("5-6+in 7+1_space 1/0_Sun 2*3Stars ray9*+3")
    result = haiku.generate_haiku()
    expected = ['5-6+', 'in', '7+1_', 'space', '1/0_', 'Err', 'Sun', '2x3', 'Stars', 'ray9*', 'Err']
    assert result == expected


def test_sci_fi_haiku_no_expression_errors():
    haiku = SciFiHaiku("2+3_5star 3+4light 6/3_Moons Venus" )
    result = haiku.generate_haiku()
    expected = ['2+3_', '5', 'star', '3+4_', 'light', '6/3_', 'Moons', 'Venus']
    assert result == expected


def test_sci_fi_haiku_single_line():
    haiku = SciFiHaiku("1000_%")
    result = haiku.generate_haiku()
    expected = ['1000_', 'Err']
    assert result == expected


def test_sci_fi_haiku_expression_only():
    haiku = SciFiHaiku("3+2 4*1 5/5")
    result = haiku.evaluate_expressions()
    expected = ['5', '4', '1']
    assert result == expected
