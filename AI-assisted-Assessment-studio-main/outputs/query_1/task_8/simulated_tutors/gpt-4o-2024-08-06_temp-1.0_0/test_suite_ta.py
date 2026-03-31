from program import *
import pytest

from program import pantheon_oracle

@pytest.mark.parametrize("adventure_logs, expected_fortune", [
    ([], 0),
    (["minotaur", "minotaur", "minotaur", "phoenix", "phoenix", "phoenix", "hydra"], 20),
    (["phoenix", "phoenix", "phoenix", "phoenix", "hydra", "hydra"], 5),
    (["minotaur", "minotaur", "minotaur", "minotaur", "minotaur", "minotaur", "minotaur"], 30),
    (["phoenix", "phoenix", "phoenix", "hydra", "hydra", "hydra", "hydra", "hydra", "hydra", "hydra", "dragon", "dragon"], 25),
    (["hydra", "hydra", "hydra", "hydra", "hydra", "hydra", "dragon", "dragon", "dragon", "wyvern", "wyvern", "wyvern", "wyvern"], 55),
])
def test_pantheon_oracle(adventure_logs, expected_fortune):
    assert pantheon_oracle(adventure_logs) == expected_fortune
