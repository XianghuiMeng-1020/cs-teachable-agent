from solution_program import *
import pytest

from solution_program import PhenomenaMonitor

@pytest.fixture
def monitor():
    return PhenomenaMonitor()


def test_add_phenomenon_and_retrieve_by_type(monitor):
    monitor.add_phenomenon({"type": "Aurora", "severity": "low", "observation_notes": []})
    monitor.add_phenomenon({"type": "Supernova", "severity": "high", "observation_notes": []})
    auroras = monitor.get_phenomena_by_type("Aurora")
    assert len(auroras) == 1
    assert auroras[0]["type"] == "Aurora"

def test_get_severity_count(monitor):
    monitor.add_phenomenon({"type": "Aurora", "severity": "low", "observation_notes": []})
    monitor.add_phenomenon({"type": "Supernova", "severity": "high", "observation_notes": []})
    monitor.add_phenomenon({"type": "Meteor Shower", "severity": "medium", "observation_notes": []})
    severity_count = monitor.get_severity_count()
    assert severity_count == {"low": 1, "medium": 1, "high": 1}

def test_add_observation(monitor):
    monitor.add_phenomenon({"type": "Aurora", "severity": "low", "observation_notes": []})
    monitor.add_observation(0, "Observed during night shift.")
    auroras = monitor.get_phenomena_by_type("Aurora")
    assert auroras[0]["observation_notes"] == ["Observed during night shift."]

def test_add_observation_invalid_index_gracefully(monitor):
    monitor.add_phenomenon({"type": "Aurora", "severity": "low", "observation_notes": []})
    monitor.add_observation(10, "Impossible observation.")  # Invalid index
    auroras = monitor.get_phenomena_by_type("Aurora")
    assert auroras[0]["observation_notes"] == []

def test_empty_severity_count(monitor):
    severity_count = monitor.get_severity_count()
    assert severity_count == {}