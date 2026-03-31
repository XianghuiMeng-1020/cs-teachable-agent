import pytest
import os
from solution import filter_mythical_creatures

filename = 'test_mythology.txt'
output_filename = 'filtered_myths_test.txt'

def setup_module(module):
    content = '''Minotaur:legendary
Nessie:myth
Kraken:legendary
Bigfoot:folklore
Phoenix:legendary
Yeti:folklore
Golem:myth
Frost_Giant:legendary
Unicorn:legends
Dragon:folklore
'''
    with open(filename, 'w') as file:
        file.write(content)


def teardown_module(module):
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)


def test_filter_legendary():
    filter_mythical_creatures(filename, output_filename, 'legendary')
    with open(output_filename, 'r') as file:
        contents = file.read()
    assert contents == "Minotaur\nKraken\nPhoenix\nFrost_Giant\n"


def test_filter_myth():
    filter_mythical_creatures(filename, output_filename, 'myth')
    with open(output_filename, 'r') as file:
        contents = file.read()
    assert contents == "Nessie\nGolem\n"


def test_filter_folklore():
    filter_mythical_creatures(filename, output_filename, 'folklore')
    with open(output_filename, 'r') as file:
        contents = file.read()
    assert contents == "Bigfoot\nYeti\nDragon\n"


def test_filter_no_creatures():
    filter_mythical_creatures(filename, output_filename, 'legend')
    with open(output_filename, 'r') as file:
        contents = file.read()
    assert contents == ""


def test_filter_partial_content():
    content = '''Centaur:legendary
Griffon:myth\nBanshee:folklore\n'''
    with open(filename, 'w') as file:
        file.write(content)
    filter_mythical_creatures(filename, output_filename, 'folklore')
    with open(output_filename, 'r') as file:
        contents = file.read()
    assert contents == "Banshee\n"
