import pytest
from solution import Spaceship

@pytest.fixture(scope="module")
def setup_module():
    return None

@pytest.fixture(scope="module")
def teardown_module():
    return None


def test_normal_trip():
    spaceship = Spaceship('Galactic Voyager', 5)
    result = spaceship.book_trip('Alpha Centauri', 20)
    assert result == "Trip to Alpha Centauri will take 4.0 hours."

def test_max_speed_zero():
    spaceship = Spaceship('Light Slug', 0)
    result = spaceship.book_trip('Proxima Centauri', 15)
    assert result == "Cannot book trip: spaceship speed is zero."

def test_distance_zero():
    spaceship = Spaceship('Cosmos Racer', 10)
    with pytest.raises(ValueError) as excinfo:
        spaceship.book_trip('Sirius', 0)
    assert "Distance must be a positive integer." in str(excinfo.value)

def test_negative_distance():
    spaceship = Spaceship('Star Hopper', 10)
    with pytest.raises(ValueError) as excinfo:
        spaceship.book_trip('Vega', -5)
    assert "Distance must be a positive integer." in str(excinfo.value)

def test_large_distance():
    spaceship = Spaceship('Galaxy Cruiser', 100000)
    result = spaceship.book_trip('Andromeda', 1000000)
    assert result == "Trip to Andromeda will take 10.0 hours."