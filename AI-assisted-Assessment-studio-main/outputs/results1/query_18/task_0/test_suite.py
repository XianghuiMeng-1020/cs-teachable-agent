import pytest
import os
from solution import calculate_avg_travel_time

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open("intergalactic_travel_test.txt", "w") as f:
        f.write("Mars,10\n")
        f.write("Mars,20\n")
        f.write("Venus,5\n")
        f.write("Venus,15\n")
        f.write("Jupiter,45\n")
        f.write("Jupiter,55\n")
    yield
    os.remove("intergalactic_travel_test.txt")
    if os.path.exists("output_test.txt"):
        os.remove("output_test.txt")

@pytest.fixture
def run_test_calculate_avg_travel_time():
    calculate_avg_travel_time("intergalactic_travel_test.txt", "output_test.txt")
    return "output_test.txt"


def test_avg_time_mars(run_test_calculate_avg_travel_time):
    with open(run_test_calculate_avg_travel_time, "r") as f:
        output = f.readlines()
    assert "Mars:15.0\n" in output


def test_avg_time_venus(run_test_calculate_avg_travel_time):
    with open(run_test_calculate_avg_travel_time, "r") as f:
        output = f.readlines()
    assert "Venus:10.0\n" in output


def test_avg_time_jupiter(run_test_calculate_avg_travel_time):
    with open(run_test_calculate_avg_travel_time, "r") as f:
        output = f.readlines()
    assert "Jupiter:50.0\n" in output


def test_total_lines(run_test_calculate_avg_travel_time):
    with open(run_test_calculate_avg_travel_time, "r") as f:
        lines = f.readlines()
    assert len(lines) == 3


def test_no_extra_entries(run_test_calculate_avg_travel_time):
    with open(run_test_calculate_avg_travel_time, "r") as f:
        content = f.read().strip()
    assert content == "Mars:15.0\nVenus:10.0\nJupiter:50.0"