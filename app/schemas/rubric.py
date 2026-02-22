"""API schemas for Rubric operations."""

from typing import Optional, List
from pydantic import BaseModel
from app.models.rubric import (
    Rubric,
    RubricType,
    EvaluationDimension,
    RubricCriteria,
    ScoringScale
)


class RubricCreate(Rubric):
    """Schema for creating a new rubric."""
    pass


class RubricUpdate(BaseModel):
    """Schema for updating a rubric."""
    name: Optional[str] = None
    rubric_type: Optional[RubricType] = None
    domain_id: Optional[str] = None
    evaluation_dimension: Optional[EvaluationDimension] = None
    description: Optional[str] = None
    criteria: Optional[List[RubricCriteria]] = None
    scoring_scale: Optional[ScoringScale] = None
    instructions: Optional[str] = None
    metadata: Optional[dict] = None


class RubricResponse(Rubric):
    """Schema for rubric response."""
    pass



