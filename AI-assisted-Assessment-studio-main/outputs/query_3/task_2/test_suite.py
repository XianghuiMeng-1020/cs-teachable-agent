import pytest
from solution_program import calculate_efficiency

def test_calculate_efficiency():
    messages1 = {
        'Alpha-1': {'Beta-2': 100, 'Delta-4': 250},
        'Beta-2': {'Alpha-1': 50},
        'Delta-4': {'Alpha-1': 100, 'Beta-2': 150}
    }
    assert calculate_efficiency(messages1) == {'Alpha-1': 0.68, 'Beta-2': 11.72, 'Delta-4': 0.49}

    messages2 = {}
    assert calculate_efficiency(messages2) == {}

    messages3 = {
        'Zeta-9': {'Epsilon-5': 90},
        'Epsilon-5': {}
    }
    assert calculate_efficiency(messages3) == {'Zeta-9': 0.33, 'Epsilon-5': 0.0}

    messages4 = {
        'Gamma-7': {'Theta-3': 320, 'Iota-11': 480},
        'Theta-3': {'Gamma-7': 210}
    }
    assert calculate_efficiency(messages4) == {'Gamma-7': 1.82, 'Theta-3': 2.61}

    messages5 = {
        'Tau99': {'Phi88': 512, 'Omega66': 128},
        'Phi88': {'Omega66': 64}
    }
    assert calculate_efficiency(messages5) == {'Tau99': 5.34, 'Phi88': 0.47}