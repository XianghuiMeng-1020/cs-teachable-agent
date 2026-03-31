from program import *
import pytest
from program import calculate_total_ingredients

def test_basic_case():
    assert calculate_total_ingredients(['flour:500', 'sugar:300', 'flour:200', 'eggs:12']) == {'flour': 700, 'sugar': 300, 'eggs': 12}

def test_with_invalid_entries():
    assert calculate_total_ingredients(['flour:500', 'sugar:300g', 'flour:200', 'eggs:12']) == {'flour': 700, 'eggs': 12}

def test_no_valid_entries():
    assert calculate_total_ingredients(['flour-', 'sugar:30g', 'flour', 'eggs:']) == {}

def test_mixed_entries():
    assert calculate_total_ingredients(['salt:50', ':100', 'pepper:30', 'salt:50g', 'pepper:20']) == {'salt': 50, 'pepper': 50}

def test_empty_list():
    assert calculate_total_ingredients([]) == {}