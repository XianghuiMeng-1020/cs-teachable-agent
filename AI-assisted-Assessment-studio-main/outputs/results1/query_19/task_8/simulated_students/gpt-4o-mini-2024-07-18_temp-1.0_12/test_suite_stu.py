from solution_program import *
import pytest
import os
from spaceship_log import log_position, retrieve_positions


def setup_module():
    log_position("2023-10-01 00:00:00", 100, 200)
    log_position("2023-10-01 00:01:00", 150, 250)


def teardown_module():
    if os.path.exists('navigation_log.txt'):
        os.remove('navigation_log.txt')


def test_log_position_creates_file():
    assert os.path.exists('navigation_log.txt')


def test_retrieve_positions_size():
    positions = retrieve_positions()
    assert len(positions) == 2


def test_retrieve_positions_content():
    positions = retrieve_positions()
    assert positions[0]['timestamp'] == "2023-10-01 00:00:00"
    assert positions[0]['x'] == 100
    assert positions[0]['y'] == 200


def test_log_additional_entry():
    log_position("2023-10-01 00:02:00", 300, 400)
    positions = retrieve_positions()
    assert len(positions) == 3
    assert positions[2]['timestamp'] == "2023-10-01 00:02:00"


def test_retrieve_positions_missing_file():
    os.remove('navigation_log.txt')
    positions = retrieve_positions()
    assert positions == []
    log_position("2023-10-01 00:03:00", 500, 600)
    positions_once_again = retrieve_positions()
    assert positions_once_again[0]['x'] == 500