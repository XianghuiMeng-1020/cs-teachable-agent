from solution_program import *
import pytest
from solution_program import Spaceship

@pytest.fixture
def spaceship():
    return Spaceship('Odyssey', 50.0, {'Alice': 'Pilot', 'Bob': 'Engineer'})

def test_initial_status(spaceship):
    report = spaceship.status_report()
    assert report['name'] == 'Odyssey'
    assert report['energy_level'] == 50.0
    assert report['crew_members'] == {'Alice': 'Pilot', 'Bob': 'Engineer'}

def test_refuel(spaceship):
    spaceship.refuel(30.0)
    assert spaceship.energy_level == 80.0
    spaceship.refuel(30.0)
    assert spaceship.energy_level == 100.0

def test_assign_crew_member(spaceship):
    spaceship.assign_crew_member('Charlie', 'Navigator')
    assert 'Charlie' in spaceship.crew_members
    assert spaceship.crew_members['Charlie'] == 'Navigator'

def test_remove_crew_member(spaceship):
    spaceship.remove_crew_member('Alice')
    assert 'Alice' not in spaceship.crew_members

    with pytest.raises(ValueError):
        spaceship.remove_crew_member('Nonexistent')

    # Ensure Bob still exists
    assert 'Bob' in spaceship.crew_members

    spaceship.remove_crew_member('Bob')
    assert 'Bob' not in spaceship.crew_members

    # Now all crew should be removed
    assert spaceship.crew_members == {}

def test_maximum_energy_level(spaceship):
    spaceship.refuel(1000)
    assert spaceship.energy_level == 100.0

    spaceship.refuel(-150)
    assert spaceship.energy_level == 0