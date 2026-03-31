from solution_program import *
import pytest
import os
from solution_program import calculate_winner_board_game

file_content_1 = """Alice:150:3
Bob:120:4
Charlie:180:2
"""

file_content_2 = """Daisy:200:4
Eve:300:6
Frank:100:2
"""

file_content_3 = """Uni:100:1
Vivi:90:3
Xander:300:5
"""

file_content_4 = """Yara:550:5
Zane:480:4
Alex:600:6
"""

file_content_5 = """Oscar:480:6
Peter:570:4
Quincy:470:2
"""

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open('test1.txt', 'w') as f:
        f.write(file_content_1)
    with open('test2.txt', 'w') as f:
        f.write(file_content_2)
    with open('test3.txt', 'w') as f:
        f.write(file_content_3)
    with open('test4.txt', 'w') as f:
        f.write(file_content_4)
    with open('test5.txt', 'w') as f:
        f.write(file_content_5)
    
    yield

    os.remove('test1.txt')
    os.remove('test2.txt')
    os.remove('test3.txt')
    os.remove('test4.txt')
    os.remove('test5.txt')

@pytest.mark.parametrize("file_path, expected_winner", [
    ('test1.txt', 'Charlie'),
    ('test2.txt', 'Frank'),
    ('test3.txt', 'Uni'),
    ('test4.txt', 'Zane'),
    ('test5.txt', 'Peter')
])
def test_calculate_winner_board_game(file_path, expected_winner):
    result = calculate_winner_board_game(file_path)
    assert result == expected_winner