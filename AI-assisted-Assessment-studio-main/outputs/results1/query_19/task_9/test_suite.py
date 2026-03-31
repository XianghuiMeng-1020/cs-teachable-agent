import pytest
import os
from solution import parse_logs

def setup_module(module):
    os.makedirs('logs', exist_ok=True)
    log_contents = {
        'star_log_1.txt': """2023-01-01 EVENT_A: First event occurred\n2023-01-01 EVENT_B: Second event occurred\n2023-01-02 EVENT_A: Another event A occurred\n""",
        'star_log_2.txt': """2023-01-03 EVENT_C: Event C occurred\n2023-01-03 EVENT_A: Another event A\n""",
        'star_log_3.txt': """2023-01-04 EVENT_B: Different event B occurred\n""",
        'some_other_file.txt': """This should not be read\n2023-01-05 EVENT_A: Event A\n"""  # Should be ignored because of filename
    }
    for filename, content in log_contents.items():
        with open(os.path.join('logs', filename), 'w') as f:
            f.write(content)


def teardown_module(module):
    file_list = os.listdir('logs')
    for filename in file_list:
        file_path = os.path.join('logs', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir('logs')
    if os.path.exists('output.txt'):
        os.remove('output.txt')


def test_parse_logs_event_a():
    parse_logs('logs', 'EVENT_A', 'output.txt')
    with open('output.txt', 'r') as f:
        result = f.read()
    expected = """2023-01-01 EVENT_A: First event occurred\n2023-01-02 EVENT_A: Another event A occurred\n2023-01-03 EVENT_A: Another event A\n"""
    assert result == expected


def test_parse_logs_event_b():
    parse_logs('logs', 'EVENT_B', 'output.txt')
    with open('output.txt', 'r') as f:
        result = f.read()
    expected = """2023-01-01 EVENT_B: Second event occurred\n2023-01-04 EVENT_B: Different event B occurred\n"""
    assert result == expected


def test_parse_logs_event_not_found():
    parse_logs('logs', 'EVENT_X', 'output.txt')
    with open('output.txt', 'r') as f:
        result = f.read()
    expected = """"
    assert result == expected


def test_parse_logs_nonexistent_file():
    os.remove('logs/star_log_2.txt')  # Simulate file removal
    parse_logs('logs', 'EVENT_A', 'output.txt')
    with open('output.txt', 'r') as f:
        result = f.read()
    expected = """2023-01-01 EVENT_A: First event occurred\n2023-01-02 EVENT_A: Another event A occurred\n"""
    assert result == expected


def test_parse_logs_empty_directory():
    for filename in os.listdir('logs'):
        os.remove(os.path.join('logs', filename))
    parse_logs('logs', 'EVENT_A', 'output.txt')
    with open('output.txt', 'r') as f:
        result = f.read()
    expected = """"
    assert result == expected
