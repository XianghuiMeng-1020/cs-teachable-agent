from program import *
import pytest
import os
from program import identify_legendary_creatures

def setup_module(module):
    with open('creatures.txt', 'w') as file:
        file.write('Minotaur 95 80\n')
        file.write('Cerberus 88 85\n')
        file.write('Phoenix 100 90\n')
        file.write('Chimera 85 75\n')
        file.write('Pegasus 70 65\n')
        file.write('Dragon 90 75\n')


def teardown_module(module):
    if os.path.exists('creatures.txt'):
        os.remove('creatures.txt')
    if os.path.exists('legendary_creatures.txt'):
        os.remove('legendary_creatures.txt')


def test_identify_legendary_creatures_base_case():
    identify_legendary_creatures('creatures.txt', 'legendary_creatures.txt')
    with open('legendary_creatures.txt', 'r') as file:
        lines = file.read().splitlines()
    assert 'Minotaur' in lines
    assert 'Phoenix' in lines
    assert 'Dragon' in lines


def test_identify_legendary_creatures_exclusion_case():
    identify_legendary_creatures('creatures.txt', 'legendary_creatures.txt')
    with open('legendary_creatures.txt', 'r') as file:
        lines = file.read().splitlines()
    assert 'Cerberus' not in lines
    assert 'Chimera' not in lines
    assert 'Pegasus' not in lines


def test_identify_legendary_creatures_edge_case_min_power_skill():
    with open('creatures_edge.txt', 'w') as file:
        file.write('Hydra 90 75\n')
    identify_legendary_creatures('creatures_edge.txt', 'legendary_creatures_2.txt')
    with open('legendary_creatures_2.txt', 'r') as file:
        lines = file.read().splitlines()
    assert 'Hydra' in lines
    os.remove('creatures_edge.txt')
    os.remove('legendary_creatures_2.txt')


def test_identify_legendary_creatures_no_legendary_case():
    with open('creatures_none.txt', 'w') as file:
        file.write('Goblin 60 40\n')
        file.write('Wisp 55 30\n')
    identify_legendary_creatures('creatures_none.txt', 'legendary_creatures_3.txt')
    with open('legendary_creatures_3.txt', 'r') as file:
        lines = file.read().splitlines()
    assert lines == []
    os.remove('creatures_none.txt')
    os.remove('legendary_creatures_3.txt')


def test_identify_legendary_creatures_all_legendary_case():
    with open('creatures_all.txt', 'w') as file:
        file.write('Zeus 99 90\n')
        file.write('Hades 95 88\n')
        file.write('Athena 94 81\n')
    identify_legendary_creatures('creatures_all.txt', 'legendary_creatures_4.txt')
    with open('legendary_creatures_4.txt', 'r') as file:
        lines = file.read().splitlines()
    assert 'Zeus' in lines
    assert 'Hades' in lines
    assert 'Athena' in lines
    os.remove('creatures_all.txt')
    os.remove('legendary_creatures_4.txt')
