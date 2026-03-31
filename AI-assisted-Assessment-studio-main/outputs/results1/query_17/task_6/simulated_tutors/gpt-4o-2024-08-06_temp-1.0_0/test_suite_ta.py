from program import *
import pytest
from program import Alien, assign_mission

def test_all_aliens_qualified():
    alien1 = Alien("Zog", "Martian", {"hacking": 5, "flying": 8})
    alien2 = Alien("Xena", "Venusian", {"hacking": 6, "flying": 8})
    aliens = [alien1, alien2]
    mission_requirements = {"hacking": 5, "flying": 7}
    result = assign_mission(aliens, mission_requirements)
    assert result == [alien1, alien2]

def test_some_aliens_qualified():
    alien1 = Alien("Zog", "Martian", {"hacking": 4, "flying": 9})
    alien2 = Alien("Xena", "Venusian", {"hacking": 6, "flying": 2})
    alien3 = Alien("Glorp", "Jupiterian", {"hacking": 5, "flying": 8})
    aliens = [alien1, alien2, alien3]
    mission_requirements = {"hacking": 5, "flying": 7}
    result = assign_mission(aliens, mission_requirements)
    assert result == [alien3]

def test_no_aliens_qualified():
    alien1 = Alien("Zog", "Martian", {"hacking": 4, "flying": 6})
    alien2 = Alien("Xena", "Venusian", {"hacking": 5, "flying": 5})
    aliens = [alien1, alien2]
    mission_requirements = {"hacking": 5, "flying": 7}
    with pytest.raises(ValueError, match="No suitable aliens found"):
        assign_mission(aliens, mission_requirements)

def test_no_skills_listed_yet_met():
    alien1 = Alien("Zog", "Martian", {})
    alien2 = Alien("Xena", "Venusian", {"hacking": 6, "flying": 2})
    aliens = [alien1, alien2]
    mission_requirements = {"hacking": 5}
    result = assign_mission(aliens, mission_requirements)
    assert result == [alien2]


def test_empty_alien_list():
    aliens = []
    mission_requirements = {"hacking": 5, "flying": 7}
    with pytest.raises(ValueError, match="No suitable aliens found"):
        assign_mission(aliens, mission_requirements)