import pytest
from solution_program import MartianConverter

@pytest.fixture(scope="module")
def setup_module():
    return MartianConverter()

@pytest.mark.parametrize("test_input,expected_output", [
    ("10", "25.00"),
    ("10.5", "26.25"),
    (" 12.3 ", "30.75"),
    ("abc", "Error: Invalid input"),
    ("-5", "Error: Invalid input"),
    ("3.14159", "7.85"),
    ("  14 ", "35.00"),
    ("100", "250.00"),
    ("2.5 ", "6.25"),
    ("", "Error: Invalid input"),
])
def test_convert_to_kilometers(setup_module, test_input, expected_output):
    converter = setup_module
    result = converter.convert_to_kilometers(test_input)
    assert result == expected_output

def teardown_module(module):
    pass