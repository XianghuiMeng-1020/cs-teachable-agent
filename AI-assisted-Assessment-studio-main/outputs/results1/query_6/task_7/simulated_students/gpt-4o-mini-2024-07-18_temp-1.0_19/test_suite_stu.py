from solution_program import *
import pytest
import os
from solution_program import MythArchive

def setup_module(module):
    os.makedirs('test_myths', exist_ok=True)
    with open('test_myths/dragon_tale.txt', 'w') as f:
        f.write('Dragon Tale\nOnce upon a fiery time...')
    with open('test_myths/phoenix_tale.txt', 'w') as f:
        f.write('Phoenix Tale\nRising from the ashes...')
    with open('test_myths/minotaur_tale.txt', 'w') as f:
        f.write('Minotaur Tale\nIn the winding labyrinth...')

def teardown_module(module):
    for file in os.listdir('myth_archive'):
        os.remove(os.path.join('myth_archive', file))
    os.rmdir('myth_archive')
    for file in os.listdir('test_myths'):
        os.remove(os.path.join('test_myths', file))
    os.rmdir('test_myths')

@pytest.fixture

def myth_archive():
    return MythArchive()

@pytest.mark.parametrize("tale_file, tale_name, expected_content", [
    ('test_myths/dragon_tale.txt', 'Dragon Tale', 'Once upon a fiery time...'),
    ('test_myths/phoenix_tale.txt', 'Phoenix Tale', 'Rising from the ashes...'),
    ('test_myths/minotaur_tale.txt', 'Minotaur Tale', 'In the winding labyrinth...')
])
def test_add_and_get_tale(myth_archive, tale_file, tale_name, expected_content):
    myth_archive.add_tale(tale_file)
    content = myth_archive.get_tale(tale_name)
    assert content == expected_content

@pytest.mark.parametrize("tale_file, added_name", [
    ('test_myths/dragon_tale.txt', 'Dragon Tale'),
    ('test_myths/phoenix_tale.txt', 'Phoenix Tale')
])
def test_list_tales(myth_archive, tale_file, added_name):
    myth_archive.add_tale(tale_file)
    tales = myth_archive.list_tales()
    assert added_name in tales

def test_remove_tale(myth_archive):
    myth_archive.add_tale('test_myths/minotaur_tale.txt')
    myth_archive.remove_tale('Minotaur Tale')
    tales = myth_archive.list_tales()
    assert 'Minotaur Tale' not in tales

@pytest.mark.parametrize("tale_name", [
    'Nonexistent Tale',
    'Another Missing Tale'
])
def test_get_nonexistent_tale(myth_archive, tale_name):
    content = myth_archive.get_tale(tale_name)
    assert content == ''

@pytest.mark.parametrize("tale_file, tale_name", [
    ('test_myths/dragon_tale.txt', 'Dragon Tale'),
    ('test_myths/phoenix_tale.txt', 'Phoenix Tale')
])
def test_remove_nonexistent_tale(myth_archive, tale_file, tale_name):
    myth_archive.add_tale(tale_file)
    myth_archive.remove_tale('Nonexistent Tale')
    tales = myth_archive.list_tales()
    assert tale_name in tales