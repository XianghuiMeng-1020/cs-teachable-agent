from solution_program import *
import pytest

from solution_program import count_danger_messages

@pytest.fixture(scope="module")
def setup_module(module):
    # Setup any necessary data if needed
    pass

@pytest.fixture(scope="module")
def teardown_module(module):
    # Cleanup after tests if needed
    pass

# Test cases

def test_no_logs():
    assert count_danger_messages([]) == 0

def test_no_danger_messages():
    assert count_danger_messages(["All systems nominal.", "Checking galaxy coordinates. No issues found."]) == 0

def test_single_log_single_danger():
    assert count_danger_messages(["Power levels falling. DANGER! Immediate attention required!"]) == 1

def test_multiple_logs():
    logs = [
        "DANGER detected in sector 7.",
        "WARNING! DANGER levels critical; stabilize magnetic fields.",
        "System reboot successful, no DANGER signals detected now.",
        "DANGER DANGER DANGER! Multiple systems failing!"
    ]
    assert count_danger_messages(logs) == 6

def test_logs_without_danger_word():
    assert count_danger_messages(["Everything is stable.", "Mission parameters are within prescribed limits."]) == 0
