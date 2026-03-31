from solution_program import *
import pytest
from solution_program import determine_weather

def test_determine_weather_sunny_day():
    readings = [10, 20, 15, 18, 9, 12, 25, 11]
    threshold = 15
    assert determine_weather(readings, threshold) == 'Calm'

def test_determine_weather_rainy_day():
    readings = [30, 31, 25, 40, 35, 30, 29, 21]
    threshold = 25
    assert determine_weather(readings, threshold) == 'Stormy'


def test_determine_weather_equal_threshold():
    readings = [5, 5, 5, 10, 14, 15, 15, 15]
    threshold = 14
    assert determine_weather(readings, threshold) == 'Calm'


def test_determine_weather_barely_stormy():
    readings = [15, 20, 25, 30, 10, 5, 2, 1]
    threshold = 5
    assert determine_weather(readings, threshold) == 'Stormy'


def test_determine_weather_no_storms():
    readings = [1, 1, 1, 1, 1, 1, 1, 1]
    threshold = 2
    assert determine_weather(readings, threshold) == 'Calm'