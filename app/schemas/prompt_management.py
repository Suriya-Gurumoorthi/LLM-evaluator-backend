"""API schemas for Prompt Management operations."""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class RubricInput(BaseModel):
    """Schema for rubric input from frontend."""
    id: str = Field(..., description="Rubric ID")
    name: str = Field(..., description="Rubric name")
    weight: float = Field(..., ge=0, le=100, description="Rubric weight (0-100)")
    description: Optional[str] = Field(None, description="Rubric description")


class TestCaseInput(BaseModel):
    """Schema for test case input from frontend."""
    id: str = Field(..., description="Test case ID")
    input: str = Field(..., min_length=1, description="Test case input")
    expectedOutput: Optional[str] = Field(None, description="Expected output (optional)")


class PromptEvaluationRequest(BaseModel):
    """Schema for prompt evaluation request."""
    domain_id: str = Field(..., description="Selected domain ID")
    rubrics: List[RubricInput] = Field(..., min_length=1, description="List of rubrics with weights")
    prompt: str = Field(..., min_length=1, description="User-entered prompt to evaluate")
    llm_model: str = Field(..., description="Selected LLM model")
    api_key: str = Field(..., min_length=1, description="API key for the selected LLM provider")
    test_cases: List[TestCaseInput] = Field(..., min_length=1, description="List of test cases")

    @field_validator("api_key", mode="before")
    @classmethod
    def normalize_api_key(cls, v: str) -> str:
        return _normalize_api_key(v)

    @classmethod
    def validate_rubric_weights(cls, rubrics: List[RubricInput]) -> bool:
        total_weight = sum(r.weight for r in rubrics)
        return abs(total_weight - 100.0) < 0.01


def _normalize_api_key(v: str) -> str:
    """Remove all whitespace from API key."""
    if isinstance(v, str):
        return "".join(v.split())
    return v


class APIKeyValidationRequest(BaseModel):
    """Schema for API key validation request."""
    llm_model: str = Field(..., description="Selected LLM model")
    api_key: str = Field(..., min_length=1, description="API key to validate")

    @field_validator("api_key", mode="before")
    @classmethod
    def normalize_api_key(cls, v: str) -> str:
        return _normalize_api_key(v)


class APIKeyValidationResponse(BaseModel):
    """Schema for API key validation response."""
    is_valid: bool = Field(..., description="Whether the API key is valid")
    message: str = Field(..., description="Validation message")
    provider: Optional[str] = Field(None, description="LLM provider name")


class PromptEvaluationResponse(BaseModel):
    """Schema for prompt evaluation response."""
    success: bool = Field(..., description="Whether the evaluation was successful")
    message: str = Field(..., description="Response message")
    evaluation_id: Optional[str] = Field(None, description="Unique identifier for this evaluation")


# ---------------------------------------------------------------------------
#  Test-case-level result (kept for backward compatibility + LLM output data)
# ---------------------------------------------------------------------------

class TestCaseResult(BaseModel):
    """Schema for individual test case evaluation result."""
    test_case_id: str = Field(..., description="Test case ID")
    test_case_index: int = Field(..., description="Test case index (1-based)")
    input: str = Field(..., description="Test case input")
    expected_output: Optional[str] = Field(None, description="Expected output if provided")
    has_expected_output: bool = Field(False, description="Whether expected output was provided")
    generated_output: Optional[str] = Field(None, description="Generated output from LLM")
    generation_success: bool = Field(False, description="Whether generation was successful")
    similarity_score: Optional[float] = Field(None, ge=0, le=1, description="Cosine similarity score (0-1)")
    is_match: Optional[bool] = Field(None, description="Whether similarity meets threshold")
    comparison_result: Optional[dict] = Field(None, description="Detailed comparison results")
    success: bool = Field(False, description="Whether test case evaluation succeeded")
    error: Optional[str] = Field(None, description="Error message if evaluation failed")


class OverallMetrics(BaseModel):
    """Schema for overall evaluation metrics."""
    total_test_cases: int = Field(..., description="Total number of test cases")
    successful_generations: int = Field(0, description="Number of successful generations")
    failed_generations: int = Field(0, description="Number of failed generations")
    test_cases_with_expected_output: int = Field(0)
    test_cases_without_expected_output: int = Field(0)
    average_similarity_score: Optional[float] = Field(None, ge=0, le=1)
    min_similarity_score: Optional[float] = Field(None, ge=0, le=1)
    max_similarity_score: Optional[float] = Field(None, ge=0, le=1)
    matches_above_threshold: int = Field(0)
    matches_below_threshold: int = Field(0)
    generation_success_rate: float = Field(0.0, ge=0, le=100)


# ---------------------------------------------------------------------------
#  LLM-as-Judge schemas
# ---------------------------------------------------------------------------

class OutputJudgeTestCaseScore(BaseModel):
    """Score for a single test case from the output quality judge."""
    test_case_index: int
    correctness: float = Field(0, ge=0, le=100)
    relevance: float = Field(0, ge=0, le=100)
    completeness: float = Field(0, ge=0, le=100)
    overall_score: float = Field(0, ge=0, le=100)
    feedback: str = ""


class OutputJudgeResult(BaseModel):
    """Result from Judge #1 – output quality analysis."""
    test_case_scores: List[OutputJudgeTestCaseScore] = Field(default_factory=list)
    overall_score: float = Field(0, ge=0, le=100)
    overall_feedback: str = ""


class PromptJudgeRubricScore(BaseModel):
    """Score for a single rubric from the prompt quality judge."""
    rubric_id: str = ""
    rubric_name: str = ""
    score: float = Field(0, ge=0, le=100)
    feedback: str = ""


class PromptJudgeResult(BaseModel):
    """Result from Judge #2 – prompt quality analysis."""
    rubric_scores: List[PromptJudgeRubricScore] = Field(default_factory=list)
    overall_score: float = Field(0, ge=0, le=100)
    overall_feedback: str = ""


# ---------------------------------------------------------------------------
#  Full evaluation results response
# ---------------------------------------------------------------------------

class EvaluationResultsResponse(BaseModel):
    """Schema for complete evaluation results."""
    evaluation_id: str = Field(..., description="Unique identifier for this evaluation")
    prompt: str = Field(..., description="The evaluated prompt")
    model_used: str = Field(..., description="LLM model used for evaluation")
    total_test_cases: int = Field(..., description="Total number of test cases")
    successful_generations: int = Field(0, description="Number of successful generations")
    test_case_results: List[TestCaseResult] = Field(default_factory=list)
    overall_metrics: OverallMetrics
    rubrics: List[dict] = Field(default_factory=list)
    domain_id: str = Field(..., description="Domain ID")
    output_judge_result: Optional[OutputJudgeResult] = Field(None, description="Output quality judge results")
    prompt_judge_result: Optional[PromptJudgeResult] = Field(None, description="Prompt quality judge results")
