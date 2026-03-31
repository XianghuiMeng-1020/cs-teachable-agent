from program import *
import pytest

from program import update_inventory

@pytest.mark.parametrize("inventory, sales, expected", [
    (   # Base case with normal processing
        {'Monopoly': 5, 'Risk': 7, 'Catan': 3},
        [('Monopoly', 2), ('Risk', 8), ('Catan', 1)],
        {'Monopoly': 3, 'Risk': 7, 'Catan': 2}
    ),
    (   # All sales possible
        {'Chess': 10, 'Checkers': 5, 'Go': 8},
        [('Chess', 5), ('Checkers', 5), ('Go', 8)],
        {'Chess': 5, 'Checkers': 0, 'Go': 0}
    ),
    (   # Sale not possible due to zero initial stock
        {'Scrabble': 0, 'Pictionary': 4},
        [('Scrabble', 1), ('Pictionary', 3)],
        {'Scrabble': 0, 'Pictionary': 1}
    ),
    (   # No sales scenario
        {'Life': 6, 'Guess Who?': 3},
        [],
        {'Life': 6, 'Guess Who?': 3}
    ),
    (   # High quantity sale, cannot be fulfilled, all left unchanged
        {'Sushi Go': 2},
        [('Sushi Go', 5)],
        {'Sushi Go': 2}
    ),
])
def test_update_inventory(inventory, sales, expected):
    assert update_inventory(inventory, sales) == expected