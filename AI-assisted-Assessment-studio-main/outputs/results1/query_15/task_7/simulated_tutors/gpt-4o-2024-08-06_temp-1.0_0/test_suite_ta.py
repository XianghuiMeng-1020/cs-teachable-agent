from program import *
import pytest

from program import check_maintenance

def test_check_maintenance_basic():
    assert check_maintenance([1000, 2000, 3002, 499]) == [
        "Check required",
        "Check required",
        "No check needed",
        "No check needed"
    ]

def test_check_maintenance_no_checks_needed():
    assert check_maintenance([199, 355, 802, 999]) == [
        "No check needed",
        "No check needed",
        "No check needed",
        "No check needed"
    ]

def test_check_maintenance_all_checks_required():
    assert check_maintenance([1000, 2000, 3000, 4000, 5000]) == [
        "Check required",
        "Check required",
        "Check required",
        "Check required",
        "Check required"
    ]

def test_check_maintenance_mixed_cases():
    assert check_maintenance([1050, 2000, 3999, 500]) == [
        "No check needed",
        "Check required",
        "No check needed",
        "No check needed"
    ]

def test_check_maintenance_large_values():
    assert check_maintenance([100000, 105000, 99999]) == [
        "Check required",
        "No check needed",
        "No check needed"
    ]