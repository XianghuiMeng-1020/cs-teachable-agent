from program import *
import pytest


def test_add_new_recipe():
    cookbook = {}
    updated_cookbook = manage_cookbook(cookbook, 'add', ('Pasta', ['noodles', 'sauce']))
    assert updated_cookbook == {'Pasta': ['noodles', 'sauce']}


def test_add_existing_recipe():
    cookbook = {'Pasta': ['noodles', 'sauce']}
    updated_cookbook = manage_cookbook(cookbook, 'add', ('Pasta', ['noodles', 'alt-sauce']))
    assert updated_cookbook == {'Pasta': ['noodles', 'sauce']}


def test_update_existing_recipe():
    cookbook = {'Pasta': ['noodles', 'sauce']}
    updated_cookbook = manage_cookbook(cookbook, 'update', ('Pasta', ['noodles', 'alt-sauce']))
    assert updated_cookbook == {'Pasta': ['noodles', 'alt-sauce']}


def test_delete_existing_recipe():
    cookbook = {'Pasta': ['noodles', 'sauce']}
    updated_cookbook = manage_cookbook(cookbook, 'delete', ('Pasta', []))
    assert updated_cookbook == {}


def test_delete_non_existing_recipe():
    cookbook = {'Pasta': ['noodles', 'sauce']}
    updated_cookbook = manage_cookbook(cookbook, 'delete', ('Cake', []))
    assert updated_cookbook == {'Pasta': ['noodles', 'sauce']}