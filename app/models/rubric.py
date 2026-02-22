"""Rubric models for dynamic evaluation criteria."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class RubricType(str, Enum):
    """Types of rubrics for different evaluation dimensions."""
    ACCURACY = "accuracy"
    REASONING = "reasoning"
    CODE_QUALITY = "code_quality"
    MATHEMATICAL_CORRECTNESS = "mathematical_correctness"
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FACTUAL_CORRECTNESS = "factual_correctness"
    CREATIVITY = "creativity"
    CUSTOM = "custom"


class EvaluationDimension(str, Enum):
    """Evaluation dimensions that can be assessed."""
    PROMPT_QUALITY = "prompt_quality"
    RESPONSE_QUALITY = "response_quality"
    OVERALL_QUALITY = "overall_quality"


class ScoringScale(BaseModel):
    """Scoring scale configuration for a rubric."""
    min_score: float = Field(0.0, description="Minimum score")
    max_score: float = Field(10.0, description="Maximum score")
    step: float = Field(0.1, description="Score increment step")
    
    @field_validator('max_score')
    @classmethod
    def validate_max_score(cls, v, info):
        if 'min_score' in info.data and v <= info.data['min_score']:
            raise ValueError("max_score must be greater than min_score")
        return v


class RubricCriteria(BaseModel):
    """Individual criteria within a rubric."""
    name: str = Field(..., description="Criteria name", min_length=1)
    description: str = Field(..., description="Detailed description of the criteria")
    weight: float = Field(1.0, description="Weight of this criteria (0.0 to 1.0)", ge=0.0, le=1.0)
    evaluation_guidelines: Optional[List[str]] = Field(None, description="Guidelines for evaluation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Code Correctness",
                "description": "Evaluates if the generated code is syntactically and logically correct",
                "weight": 0.4,
                "evaluation_guidelines": [
                    "Check for syntax errors",
                    "Verify logical correctness",
                    "Test edge cases"
                ]
            }
        }


class Rubric(BaseModel):
    """Dynamic rubric model for evaluation."""
    
    id: Optional[str] = Field(None, description="Unique identifier for the rubric")
    name: str = Field(..., description="Rubric name", min_length=1, max_length=100)
    rubric_type: RubricType = Field(..., description="Type of rubric")
    domain_id: Optional[str] = Field(None, description="Associated domain ID")
    evaluation_dimension: EvaluationDimension = Field(
        ..., 
        description="Which dimension this rubric evaluates"
    )
    description: Optional[str] = Field(None, description="Rubric description", max_length=500)
    criteria: List[RubricCriteria] = Field(..., description="List of evaluation criteria", min_length=1)
    scoring_scale: ScoringScale = Field(
        default_factory=lambda: ScoringScale(),
        description="Scoring scale configuration"
    )
    instructions: Optional[str] = Field(None, description="Evaluation instructions for LLM")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @field_validator('criteria')
    @classmethod
    def validate_criteria_weights(cls, v):
        """Validate that criteria weights sum to a reasonable range."""
        total_weight = sum(c.weight for c in v)
        if total_weight == 0:
            raise ValueError("At least one criteria must have a weight > 0")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "rubric_001",
                "name": "Code Generation Accuracy",
                "rubric_type": "code_quality",
                "domain_id": "domain_001",
                "evaluation_dimension": "response_quality",
                "description": "Evaluates the accuracy and quality of generated code",
                "criteria": [
                    {
                        "name": "Syntax Correctness",
                        "description": "Code must be syntactically correct",
                        "weight": 0.3,
                        "evaluation_guidelines": ["Check for syntax errors", "Verify imports"]
                    },
                    {
                        "name": "Logical Correctness",
                        "description": "Code must solve the problem correctly",
                        "weight": 0.4,
                        "evaluation_guidelines": ["Test with sample inputs", "Check edge cases"]
                    },
                    {
                        "name": "Code Quality",
                        "description": "Code should follow best practices",
                        "weight": 0.3,
                        "evaluation_guidelines": ["Check naming conventions", "Verify documentation"]
                    }
                ],
                "scoring_scale": {
                    "min_score": 0.0,
                    "max_score": 10.0,
                    "step": 0.1
                },
                "instructions": "Evaluate the code based on syntax, logic, and quality standards.",
                "metadata": {}
            }
        }

