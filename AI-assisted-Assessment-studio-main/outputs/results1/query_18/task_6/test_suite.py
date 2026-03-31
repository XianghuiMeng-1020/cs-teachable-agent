import pytest
import os
from solution import calculate_gravitational_force

G_CONSTANT = 6.67430e-11

def setup_module(module):
    input_data = [
        "5.97e24,1.496e11,6.39e23\n",
        "6.39e23,5.789e10,5.97e24\n",
        "1.898e27,7.785e11,5.97e24\n",
        "3.302e23,57900000,5.97e24\n",
        "5.68e26,1.429e12,5.97e24\n"
    ]
    with open('test_input.txt', 'w') as f:
        f.writelines(input_data)


def teardown_module(module):
    os.remove('test_input.txt')
    if os.path.exists('test_output.txt'):
        os.remove("test_output.txt")


def test_gravitational_force_calculation():
    calculate_gravitational_force('test_input.txt', 'test_output.txt')

    expected_forces = [
        (G_CONSTANT * 5.97e24 * 6.39e23) / (1.496e11 ** 2),
        (G_CONSTANT * 6.39e23 * 5.97e24) / (5.789e10 ** 2),
        (G_CONSTANT * 1.898e27 * 5.97e24) / (7.785e11 ** 2),
        (G_CONSTANT * 3.302e23 * 5.97e24) / (57900000 ** 2),
        (G_CONSTANT * 5.68e26 * 5.97e24) / (1.429e12 ** 2)
    ]
    # Formatting expected values to two decimal places
    formatted_expected_forces = ["{:.2f}".format(force) for force in expected_forces]

    with open('test_output.txt', 'r') as f:
        results = f.readlines()

    assert len(results) == len(formatted_expected_forces)
    for result, expected in zip(results, formatted_expected_forces):
        assert result.strip() == expected
