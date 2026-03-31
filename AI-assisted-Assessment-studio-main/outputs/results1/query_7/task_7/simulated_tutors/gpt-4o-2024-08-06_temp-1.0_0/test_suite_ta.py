from program import *
import pytest
import os
from program import count_creatures

input_filename = 'creatures.txt'
output_filename = 'output.txt'

def setup_module(module):
    with open(input_filename, 'w') as f:
        f.write('Fire Drake - Dragon\n')
        f.write('Ice Phoenix - Phoenix\n')
        f.write('Storm Griffin - Griffin\n')
        f.write('Lake Dragon - Dragon\n')
        f.write('Earth Drake - Dragon\n')
        f.write('Sky Phoenix - Phoenix\n')
        f.write('Mountain Griffin - Griffin\n')
        f.write('Wind Griffin - Griffin\n')
        f.write('Forest Dragon - Dragon\n')

def teardown_module(module):
    os.remove(input_filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)

@pytest.mark.parametrize("expected_content", [
    "Dragon: 4\nPhoenix: 2\nGriffin: 3\n",
    "Griffin: 3\nDragon: 4\nPhoenix: 2\n",
    "Phoenix: 2\nGriffin: 3\nDragon: 4\n",
    "Dragon: 4\nGriffin: 3\nPhoenix: 2\n",
    "Phoenix: 2\nDragon: 4\nGriffin: 3\n",
])
def test_count_creatures(expected_content):
    count_creatures(input_filename, output_filename)
    with open(output_filename) as f:
        output_content = f.read()
    assert output_content == expected_content