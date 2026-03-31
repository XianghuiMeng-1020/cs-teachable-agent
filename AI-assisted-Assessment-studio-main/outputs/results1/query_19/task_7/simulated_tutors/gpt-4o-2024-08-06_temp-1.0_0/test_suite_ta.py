from program import *
import pytest
import os
from program import analyze_weather

station_data = {
    'Station1.txt': "15.5\n16.0\n14.2\n18.9\n19.1",
    'Station2.txt': "30.0\n29.5\n31.2",
    'Station3.txt': "17.8\n18.2\n",
    'Station4.txt': "33.0\n32.5\n31.0\n",
    'Station5.txt': "32.5\nanotemp\n31.0\n"   # Corrupted line with text
}


def setup_module(module):
    for filename, content in station_data.items():
        with open(filename, 'w') as f:
            f.write(content)


def teardown_module(module):
    for filename in station_data.keys():
        os.remove(filename)


def test_station1_average():
    assert analyze_weather(1) == 16.74  # Average: (15.5+16.0+14.2+18.9+19.1)/5


def test_station2_average():
    assert analyze_weather(2) == 30.23  # Average: (30.0+29.5+31.2)/3


def test_station3_average():
    assert analyze_weather(3) == 18.0  # Average: (17.8+18.2)/2


def test_station4_average():
    assert analyze_weather(4) == 32.17  # Average: (33.0+32.5+31.0)/3


def test_station5_corrupted_data():
    assert analyze_weather(5).startswith('Error: ')  # Error due to corrupt data on line 2
