import pytest
import os
from solution import MythologyDatabase

def setup_module(module):
    with open('mythology_db.txt', 'w') as f:
        f.write('Zeus;Sky;Greek\n')
        f.write('Odin;Wisdom;Norse\n')
        f.write('Ra;Sun;Egyptian\n')

def teardown_module(module):
    try:
        os.remove('mythology_db.txt')
    except FileNotFoundError:
        pass

# Test Cases

def test_add_god():
    db = MythologyDatabase()
    db.load_from_file('mythology_db.txt')
    db.add_god('Thor', 'Thunder', 'Norse')
    assert db.search_god('Thor') == 'Thor;Thunder;Norse'


def test_remove_god():
    db = MythologyDatabase()
    db.load_from_file('mythology_db.txt')
    db.remove_god('Zeus')
    assert db.search_god('Zeus') == 'Not Found'


def test_search_god():
    db = MythologyDatabase()
    db.load_from_file('mythology_db.txt')
    assert db.search_god('Odin') == 'Odin;Wisdom;Norse'
    assert db.search_god('Apollo') == 'Not Found'


def test_save_to_file():
    db = MythologyDatabase()
    db.add_god('Freya', 'Love', 'Norse')
    db.save_to_file('test_mythology_db.txt')
    with open('test_mythology_db.txt', 'r') as f:
        data = f.read()
    assert 'Freya;Love;Norse' in data
    os.remove('test_mythology_db.txt')


def test_load_from_file():
    db = MythologyDatabase()
    db.load_from_file('mythology_db.txt')
    assert db.search_god('Ra') == 'Ra;Sun;Egyptian'
