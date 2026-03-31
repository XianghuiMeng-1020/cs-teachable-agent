from program import *
import pytest
import os
from program import find_longest_legend

def setup_module(module):
    with open('mythology_legends.txt', 'w') as f:
        f.write('Achilles\nHis strength is unparalleled. Known as the hero of the Trojan War.\nEND\n')
        f.write('Hercules\nThis son of Zeus is famous for his incredible strength and for completing the Twelve Labors.\nEND\n')
        f.write('Thor\nThe hammer-wielding god associated with thunder protects the Norse gods. His might is unchallenged.\nEND\n')
        f.write('Athena\nGoddess of wisdom, courage, and warfare, Athena is revered for her strategic skill in battle.\nEND\n')


def teardown_module(module):
    try:
        os.remove('mythology_legends.txt')
        os.remove('longest_legend.txt')
    except OSError:
        pass


def test_longest_legend():
    find_longest_legend('mythology_legends.txt', 'longest_legend.txt')
    with open('longest_legend.txt', 'r') as f:
        content = f.read()
    assert content.startswith('Hercules\n')


def test_longest_legend_content():
    find_longest_legend('mythology_legends.txt', 'longest_legend.txt')
    with open('longest_legend.txt', 'r') as f:
        content = f.read()
    assert 'Hercules' in content
    assert 'Twelve Labors' in content


def test_output_file_creation():
    find_longest_legend('mythology_legends.txt', 'longest_legend.txt')
    assert os.path.exists('longest_legend.txt')


def test_correct_handling_of_lines():
    find_longest_legend('mythology_legends.txt', 'longest_legend.txt')
    with open('longest_legend.txt', 'r') as f:
        content = f.read().strip().split('\n')
    assert len(content) == 3


def test_legend_word_count():
    with open('mythology_legends.txt', 'w') as f:
        f.write('Odin\nFather of the Aesir, deity of war and poetry.\nEND\n')
        f.write('Hera\nQueen of the gods, protector of marriage. Known for her jealousy and vindictiveness.\nEND\n')
    find_longest_legend('mythology_legends.txt', 'longest_legend.txt')
    with open('longest_legend.txt', 'r') as f:
        content = f.read()
    assert content.startswith('Hera\n')