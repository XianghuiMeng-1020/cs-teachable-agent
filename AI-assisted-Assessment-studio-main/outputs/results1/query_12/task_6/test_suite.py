import pytest
import os
from solution import organize_recipes


def setup_module(module):
    with open('recipes_test.txt', 'w') as f:
        f.write("Pancakes\nOmelette\nSpaghetti\nSalad\nSoup\n")


def teardown_module(module):
    os.remove('recipes_test.txt')
    if os.path.exists('favorite_recipes.txt'):
        os.remove('favorite_recipes.txt')
    if os.path.exists('to_try_recipes.txt'):
        os.remove('to_try_recipes.txt')
    if os.path.exists('disliked_recipes.txt'):
        os.remove('disliked_recipes.txt')


def simulate_input(inputs):
    def mock_input(prompt):
        return inputs.pop(0)
    return mock_input


def test_organize_recipes_favorite():
    user_inputs = ['Favorite', 'Favorite', 'Favorite', 'Favorite', 'Favorite']
    input_function = simulate_input(user_inputs)
    original_input = __builtins__.input
    __builtins__.input = input_function
    try:
        organize_recipes('recipes_test.txt')
        with open('favorite_recipes.txt', 'r') as f:
            content = f.read()
        assert content == "Pancakes\nOmelette\nSpaghetti\nSalad\nSoup\n"
    finally:
        __builtins__.input = original_input


def test_organize_recipes_different_categories():
    user_inputs = ['Favorite', 'To Try', 'Disliked', 'Favorite', 'To Try']
    input_function = simulate_input(user_inputs)
    original_input = __builtins__.input
    __builtins__.input = input_function
    try:
        organize_recipes('recipes_test.txt')
        with open('favorite_recipes.txt', 'r') as f:
            content_fav = f.read()
        with open('to_try_recipes.txt', 'r') as f:
            content_try = f.read()
        with open('disliked_recipes.txt', 'r') as f:
            content_dislike = f.read()
        assert content_fav == "Pancakes\nSalad\n"
        assert content_try == "Omelette\nSoup\n"
        assert content_dislike == "Spaghetti\n"
    finally:
        __builtins__.input = original_input


def test_organize_recipes_all_disliked():
    user_inputs = ['Disliked', 'Disliked', 'Disliked', 'Disliked', 'Disliked']
    input_function = simulate_input(user_inputs)
    original_input = __builtins__.input
    __builtins__.input = input_function
    try:
        organize_recipes('recipes_test.txt')
        with open('disliked_recipes.txt', 'r') as f:
            content = f.read()
        assert content == "Pancakes\nOmelette\nSpaghetti\nSalad\nSoup\n"
    finally:
        __builtins__.input = original_input


def test_organize_recipes_invalid_then_valid():
    user_inputs = ['Invalid', 'Favorite', 'Invalid', 'To Try', 'Favorite', 'Invalid', 'Invalid', 'Disliked', 'Favorite', 'To Try']
    input_function = simulate_input(user_inputs)
    original_input = __builtins__.input
    __builtins__.input = input_function
    try:
        organize_recipes('recipes_test.txt')
        with open('favorite_recipes.txt', 'r') as f:
            content_fav = f.read()
        with open('to_try_recipes.txt', 'r') as f:
            content_try = f.read()
        with open('disliked_recipes.txt', 'r') as f:
            content_dislike = f.read()
        assert content_fav == "Pancakes\nSalad\n"
        assert content_try == "Omelette\nSoup\n"
        assert content_dislike == "Spaghetti\n"
    finally:
        __builtins__.input = original_input


def test_organize_recipes_all_to_try():
    user_inputs = ['To Try', 'To Try', 'To Try', 'To Try', 'To Try']
    input_function = simulate_input(user_inputs)
    original_input = __builtins__.input
    __builtins__.input = input_function
    try:
        organize_recipes('recipes_test.txt')
        with open('to_try_recipes.txt', 'r') as f:
            content = f.read()
        assert content == "Pancakes\nOmelette\nSpaghetti\nSalad\nSoup\n"
    finally:
        __builtins__.input = original_input
