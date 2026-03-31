import pytest
from solution import active_starships

def test_all_operational():
    log_lines = ["Aegis 70", "Colossus 80", "Vanguard 90"]
    assert active_starships(log_lines) == ["Aegis", "Colossus", "Vanguard"]

def test_some_operational():
    log_lines = ["Hyperion 50", "Phoenix 40", "Nova 60"]
    assert active_starships(log_lines) == ["Nova"]

def test_none_operational():
    log_lines = ["Pioneer 30", "Odyssey 40", "Endurance 50"]
    assert active_starships(log_lines) == []

def test_mixed_order():
    log_lines = ["Falcon 55", "Ranger 45", "Eclipse 60", "Galaxy 70"]
    assert active_starships(log_lines) == ["Eclipse", "Falcon", "Galaxy"]

def test_single_entry():
    log_lines = ["Voyager 55"]
    assert active_starships(log_lines) == ["Voyager"]