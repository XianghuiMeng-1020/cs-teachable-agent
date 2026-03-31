import pytest
from solution import vegetable_counter

@pytest.mark.parametrize("order, expected", [
    (["salad: tomato=2, cucumber=1", "stir_fry: carrot=3, tomato=1"], "['carrot=3', 'cucumber=1', 'tomato=3']"),
    (["pasta: tomato=4, basil=1", "soup: carrot=2, basil=1, tomato=1"], "['basil=2', 'carrot=2', 'tomato=5']"),
    (["pizza: mushroom=5, onion=3", "sandwich: onion=2, mushroom=1"], "['mushroom=6', 'onion=5']"),
    (["curry: potato=3, pea=2", "stew: pea=3, carrot=2, potato=1"], "['carrot=2', 'pea=5', 'potato=4']"),
    (["omelet: egg=2, onion=1", "salad: egg=1, lettuce=3"], "['egg=3', 'lettuce=3', 'onion=1']")
])
def test_vegetable_counter(order, expected):
    assert vegetable_counter(order) == expected
