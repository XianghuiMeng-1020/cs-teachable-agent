import pytest
import os
from solution_program import Mythology


def setup_module(module):
    with open('mythology_stories.txt', 'w') as f:
        f.write("""
# Story Title: Zeus and the Thunderbolt
Zeus, the king of the Greek gods, was known for many mythological exploits...
# Story Title: The Odyssey
Odysseus, the hero of The Odyssey, encountered many challenges...
# Story Title: The Labors of Hercules
Ever obliging, Hercules completed many impossible tasks...
# Story Title: The Trickery of Loki
Loki, the cunning trickster of Norse mythology, was infamous for his deceptions...
# Story Title: The Phoenix's Rebirth
The Phoenix, a symbol of renewal and rebirth, rises from its ashes every 500 years...
""")


def teardown_module(module):
    try:
        os.remove('mythology_stories.txt')
        os.remove('zeus_story.txt')
        os.remove('odyssey_story.txt')
    except OSError:
        pass


def test_get_single_story():
    mythology = Mythology()
    result = mythology.get_story(['Zeus and the Thunderbolt'])
    expected = ['Zeus, the king of the Greek gods, was known for many mythological exploits...']
    assert result == expected


def test_get_multiple_stories():
    mythology = Mythology()
    result = mythology.get_story(['Zeus and the Thunderbolt', 'The Trickery of Loki'])
    expected = ['Zeus, the king of the Greek gods, was known for many mythological exploits...',
                'Loki, the cunning trickster of Norse mythology, was infamous for his deceptions...']
    assert result == expected


def test_get_non_existing_story():
    mythology = Mythology()
    result = mythology.get_story(['Non-existent Story'])
    expected = []
    assert result == expected


def test_save_story_to_file():
    mythology = Mythology()
    mythology.save_story_to_file('The Odyssey', 'odyssey_story.txt')
    with open('odyssey_story.txt', 'r') as f:
        content = f.read().strip()
    expected = 'Odysseus, the hero of The Odyssey, encountered many challenges...'
    assert content == expected


def test_save_story_does_not_overwrite():
    mythology = Mythology()
    mythology.save_story_to_file('Zeus and the Thunderbolt', 'zeus_story.txt')
    mythology.save_story_to_file('The Odyssey', 'zeus_story.txt')  # attempt to overwrite
    with open('zeus_story.txt', 'r') as f:
        content = f.read().strip()
    expected = 'Zeus, the king of the Greek gods, was known for many mythological exploits...'
    assert content == expected
