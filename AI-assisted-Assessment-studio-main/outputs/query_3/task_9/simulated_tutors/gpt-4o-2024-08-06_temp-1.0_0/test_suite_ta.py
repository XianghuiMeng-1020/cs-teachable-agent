from program import *
import pytest
from program import alien_signal_count

signal_logs_1 = {
    'Mars': ['beep', 'boop', 'beep', 'beep', 'boop'],
    'Venus': ['buzz', 'bop', 'buzz'],
    'Jupiter': [],
    'Saturn': ['zap', 'zip', 'zap', 'zip', 'zip']
}

signal_logs_2 = {
    'Earth': ['hello', 'hello'],
    'Neptune': ['gurgle', 'glurp', 'gurgle'],
    'Pluto': ['ping', 'pong']
}

signal_logs_3 = {
    'AlphaCentauri': ['sing', 'song', 'ding', 'dong', 'sing', 'song'],
}

signal_logs_4 = {
    'Tatooine': ['woosh', 'growl', 'woosh'],
    'Hoth': []
}

@pytest.mark.parametrize("inputs, expected", [
    (signal_logs_1, {
        'Mars': {'beep': 3, 'boop': 2},
        'Venus': {'buzz': 2, 'bop': 1},
        'Jupiter': {},
        'Saturn': {'zap': 2, 'zip': 3}
    }),
    (signal_logs_2, {
        'Earth': {'hello': 2},
        'Neptune': {'gurgle': 2, 'glurp': 1},
        'Pluto': {'ping': 1, 'pong': 1}
    }),
    (signal_logs_3, {
        'AlphaCentauri': {'sing': 2, 'song': 2, 'ding': 1, 'dong': 1}
    }),
    (signal_logs_4, {
        'Tatooine': {'woosh': 2, 'growl': 1},
        'Hoth': {}
    }),
    ({}, {}),
])
def test_alien_signal_count(inputs, expected):
    assert alien_signal_count(inputs) == expected
