"""AI Experiments API routes."""

from fastapi import APIRouter, Depends
from src.api.deps import CurrentUser
from src.core.ai_experiments import run_ai_experiment

router = APIRouter(prefix="/api/ai-experiments", tags=["ai-experiments"])


@router.post("/optimize-prompt")
def optimize_prompt(
    data: dict,
    current_user: CurrentUser,
):
    """Optimize a prompt using LLM-based enhancement."""
    return run_ai_experiment(
        experiment_type="optimize_prompt",
        input_data=data,
        domain=data.get("domain", "general")
    )


@router.post("/token-analysis")
def analyze_tokens(
    data: dict,
    current_user: CurrentUser,
):
    """Analyze token usage for a given text."""
    return run_ai_experiment(
        experiment_type="token_analysis",
        input_data=data,
    )


@router.post("/compare-responses")
def compare_responses(
    data: dict,
    current_user: CurrentUser,
):
    """Compare two AI responses with detailed analysis."""
    return run_ai_experiment(
        experiment_type="compare_responses",
        input_data=data,
    )
