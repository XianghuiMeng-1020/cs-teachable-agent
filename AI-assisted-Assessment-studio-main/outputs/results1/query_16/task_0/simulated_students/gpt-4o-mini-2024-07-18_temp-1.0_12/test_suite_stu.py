from solution_program import *
import pytest
from solution_program import FuelStation


def test_initial_fuel_negative():
    with pytest.raises(ValueError):
        FuelStation("Mars", -10)


def test_refuel_negative_amount():
    station = FuelStation("Mars", 100)
    with pytest.raises(ValueError):
        station.refuel(-50)


def test_consume_exact_amount():
    station = FuelStation("Venus", 200)
    station.consume(200)
    assert station.get_fuel_report() == "Fuel station on Venus has 0 gallons left."


def test_consume_excess_fuel():
    station = FuelStation("Jupiter", 150)
    with pytest.raises(Exception) as excinfo:
        station.consume(200)
    assert str(excinfo.value) == "Insufficient fuel"


def test_fuel_report_after_operations():
    station = FuelStation("Saturn", 300)
    station.refuel(100)
    station.consume(250)
    assert station.get_fuel_report() == "Fuel station on Saturn has 150 gallons left."


def test_refuel_and_consume_multiple():
    station = FuelStation("Uranus", 50)
    station.refuel(30)
    assert station.get_fuel_report() == "Fuel station on Uranus has 80 gallons left."
    station.consume(40)
    assert station.get_fuel_report() == "Fuel station on Uranus has 40 gallons left."
    with pytest.raises(Exception) as excinfo:
        station.consume(50)
    assert "Insufficient fuel" in str(excinfo.value)