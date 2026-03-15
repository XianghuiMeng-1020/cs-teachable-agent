"""A/B experiment: get condition for current user."""

from fastapi import APIRouter, Depends

from src.api.deps import CurrentUser
from src.core.experiment import get_condition_for_user

router = APIRouter(prefix="/api/experiment", tags=["experiment"])


@router.get("/condition")
def get_condition(current_user: CurrentUser):
    """Return the experiment condition for the current user (control, treatment_teaching_helper, treatment_mode_shift)."""
    return {"condition": get_condition_for_user(current_user.id)}
