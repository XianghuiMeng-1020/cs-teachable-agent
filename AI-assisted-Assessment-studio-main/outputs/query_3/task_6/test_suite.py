import pytest
from solution import dispatch_cargo

@pytest.fixture(scope="module")
def setup_module():
    pass

@pytest.fixture(scope="module")
def teardown_module():
    pass

@pytest.mark.parametrize("cargo_requests,expected", [
    ({'Andromeda': 5, 'MilkyWay': 2, 'Triangulum': 3}, {'systems_with_cargo': 3, 'leftover_cargo': 0}),
    ({'Sirius': 0, 'Proxima': 4, 'AlphaCentauri': 6}, {'systems_with_cargo': 2, 'leftover_cargo': 0}),
    ({'Orion': 10, 'Draco': 10, 'Aquarius': 0}, {'systems_with_cargo': 2, 'leftover_cargo': 0}),
    ({}, {'systems_with_cargo': 0, 'leftover_cargo': 0}),
    ({'Pegasus': 100}, {'systems_with_cargo': 1, 'leftover_cargo': 0}),
    ({'Cygnus': 5, 'Lyra': 0}, {'systems_with_cargo': 1, 'leftover_cargo': 0}),
    ({'Hydra': 8, 'Phoenix': 15, 'Cancer': 7}, {'systems_with_cargo': 3, 'leftover_cargo': 0}),
    ({'Leo': 1, 'Libra': 1, 'Virgo': 1}, {'systems_with_cargo': 3, 'leftover_cargo': 0})
])
def test_dispatch_cargo(cargo_requests, expected):
    assert dispatch_cargo(cargo_requests) == expected