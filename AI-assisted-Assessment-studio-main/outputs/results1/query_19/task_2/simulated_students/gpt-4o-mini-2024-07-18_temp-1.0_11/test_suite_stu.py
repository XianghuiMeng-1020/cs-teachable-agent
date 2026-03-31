from solution_program import *
import pytest
import os
from solution_program import read_log_file

log_file_1 = "test_log_1.txt"
log_file_2 = "test_log_2.txt"
log_file_3 = "test_log_3.txt"

log_content_1 = '''
2149-07-13 23:45:01 - Engine power boosted
2149-07-14 00:00:01 - Entered warp speed
2149-07-14 00:03:20 - Exited warp speed
'''

log_content_2 = '''
2149-07-15 12:00:00 - Initiated landing sequence
2149-07-14 09:15:01 - Docked at space station
2149-07-13 22:55:45 - Left Mars orbit
'''

log_content_3 = '''
2150-01-01 00:00:01 - New Year fireworks in orbit
2149-12-31 23:59:59 - Countdown started
2149-12-31 12:30:45 - Final maintenance check
'''

invalid_log_file = "non_existing_file.txt"

@pytest.fixture(autouse=True)
def setup_module():
    with open(log_file_1, 'w') as f:
        f.write(log_content_1)
    with open(log_file_2, 'w') as f:
        f.write(log_content_2)
    with open(log_file_3, 'w') as f:
        f.write(log_content_3)

@pytest.fixture(autouse=True)
def teardown_module():
    os.remove(log_file_1)
    os.remove(log_file_2)
    os.remove(log_file_3)

class TestReadLogFile:
    def test_correct_log_parsing(self):
        result = read_log_file(log_file_1)
        assert result == [
            "Engine power boosted",
            "Entered warp speed",
            "Exited warp speed"
        ]

    def test_unordered_log_file(self):
        result = read_log_file(log_file_2)
        assert result == [
            "Left Mars orbit",
            "Docked at space station",
            "Initiated landing sequence"
        ]

    def test_unordered_entries(self):
        result = read_log_file(log_file_3)
        assert result == [
            "Final maintenance check",
            "Countdown started",
            "New Year fireworks in orbit"
        ]

    def test_non_existing_file(self):
        result = read_log_file(invalid_log_file)
        assert result == []

    def test_empty_file(self):
        empty_log_file = "empty_log.txt"
        open(empty_log_file, 'a').close()
        result = read_log_file(empty_log_file)
        os.remove(empty_log_file)
        assert result == []
