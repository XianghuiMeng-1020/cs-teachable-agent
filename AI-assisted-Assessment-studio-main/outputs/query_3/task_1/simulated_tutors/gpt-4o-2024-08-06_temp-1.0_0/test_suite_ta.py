from program import *
import pytest

from program import sort_space_stations

def test_sort_space_stations_basic():
    example_stations = {3: "Alpha Base", 14: "Gamma Outpost", 1: "Earth Station"}
    expected_output = {
        'Human 1': 'Earth Station',
        'Human 3': 'Alpha Base',
        'Teklar 14': 'Gamma Outpost'
    }
    assert sort_space_stations(example_stations) == expected_output


def test_sort_space_stations_cupholder_empty():
    example_stations = {}
    expected_output = {}
    assert sort_space_stations(example_stations) == expected_output


def test_sort_space_stations_edge_case():
    example_stations = {999: "Omega", 2: "Beta"}
    expected_output = {
        'Teklar 2': 'Beta',
        'Human 999': 'Omega'
    }
    assert sort_space_stations(example_stations) == expected_output


def test_sort_space_stations_same_letter():
    example_stations = {8: "Alpha", 7: "Beta", 6: "Gamma", 5: "Omega"}
    expected_output = {
        'Human 5': 'Omega',
        'Human 7': 'Beta',
        'Teklar 6': 'Gamma',
        'Teklar 8': 'Alpha'
    }
    assert sort_space_stations(example_stations) == expected_output


def test_sort_space_stations_large_order():
    example_stations = {101: "Xerxes", 202: "Lunar", 303: "Venus", 404: "Olympus"}
    expected_output = {
        'Human 101': 'Xerxes',
        'Human 303': 'Venus',
        'Teklar 202': 'Lunar',
        'Teklar 404': 'Olympus'
    }
    assert sort_space_stations(example_stations) == expected_output