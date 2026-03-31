from solution_program import *
import pytest
import os
from solution_program import filter_mythical_creatures

INPUT_FILE = 'mythical_creatures.txt'
OUTPUT_FILE = 'filtered_creatures.txt'


def setup_module(module):
    with open(INPUT_FILE, 'w') as file:
        file.write("""Cerberus:Greek:Monster:A three-headed dog guarding Hades
Fenrir:Norse:Monster:A giant wolf
Achilles:Greek:Hero:A hero of the Trojan War
Thor:Norse:God:The god of thunder
Rama:Hindu:Hero:The king of Ayodhya
""")

def teardown_module(module):
    os.remove(INPUT_FILE)
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


def test_filter_by_greek_origin():
    filter_mythical_creatures(INPUT_FILE, OUTPUT_FILE, 'Greek')
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()
    assert content == "Cerberus:Greek:Monster:A three-headed dog guarding Hades\nAchilles:Greek:Hero:A hero of the Trojan War"


def test_filter_by_norse_origin():
    filter_mythical_creatures(INPUT_FILE, OUTPUT_FILE, 'Norse')
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()
    assert content == "Fenrir:Norse:Monster:A giant wolf\nThor:Norse:God:The god of thunder"


def test_filter_by_hindu_origin():
    filter_mythical_creatures(INPUT_FILE, OUTPUT_FILE, 'Hindu')
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()
    assert content == "Rama:Hindu:Hero:The king of Ayodhya"


def test_filter_with_no_match():
    filter_mythical_creatures(INPUT_FILE, OUTPUT_FILE, 'Egyptian')
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()
    assert content == ""


def test_filter_case_sensitivity():
    filter_mythical_creatures(INPUT_FILE, OUTPUT_FILE, 'greek')
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()
    assert content == ""