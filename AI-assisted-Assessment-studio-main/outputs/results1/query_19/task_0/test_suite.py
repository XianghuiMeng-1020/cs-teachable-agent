import pytest
import os

def setup_module(module):
    with open('spaceship_logs.txt', 'w') as f:
        f.write("""
Starship100:Mars:Discovered ancient ruins
Starship200:Jupiter:Detected unusual energy signatures
Starship100:Mars:Discovered ancient ruins
Starship100:Venus:Found signs of water
Starship200:Jupiter:Detected unusual energy signatures
Starship300:Earth:Traces of biological activity
Starship100:Mars:Detected high levels of radiation
Starship300:Earth:Traces of biological activity
Starship100:Venus:Found signs of water
""".strip())

def teardown_module(module):
    try:
        os.remove('spaceship_logs.txt')
        os.remove('summary.txt')
    except OSError:
        pass

def test_summary_file_creation():
    summarize_observations()
    assert os.path.exists('summary.txt')

def test_starship100_observations():
    summarize_observations()
    with open('summary.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Starship100" in line:
            assert line.strip() == 'Starship100:3'

def test_starship200_observations():
    summarize_observations()
    with open('summary.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Starship200" in line:
            assert line.strip() == 'Starship200:1'


def test_starship300_observations():
    summarize_observations()
    with open('summary.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Starship300" in line:
            assert line.strip() == 'Starship300:1'

def test_empty_logs_handling():
    with open('spaceship_logs.txt', 'w') as f:
        f.write("")
    summarize_observations()
    with open('summary.txt', 'r') as f:
        assert f.read().strip() == ""