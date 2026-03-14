"""
Stage F: Interaction Engine — thin facade over shared-cycle orchestration.

Per SHARED_CORE_ARCHITECTURE §5 and §14: the Interaction Engine orchestrates
teach → respond → test → reflect by calling the other engines in order.
This module exposes that orchestration; the actual cycle is implemented in run_cycle.
"""

from run_cycle import (
    run_teaching_and_test,
    run_correction,
    run_relearning_step,
    run_test_only,
)

__all__ = [
    "run_teaching_and_test",
    "run_correction",
    "run_relearning_step",
    "run_test_only",
]
