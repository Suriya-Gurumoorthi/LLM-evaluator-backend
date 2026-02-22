"""API routes for prompt management."""

from fastapi import APIRouter, HTTPException
from app.schemas.prompt_management import (
    PromptEvaluationRequest,
    PromptEvaluationResponse,
    APIKeyValidationRequest,
    APIKeyValidationResponse,
    EvaluationResultsResponse
)
from app.services.prompt_management_service import prompt_management_service

router = APIRouter()


@router.post("/validate-api-key", response_model=APIKeyValidationResponse)
async def validate_api_key(request: APIKeyValidationRequest):
    """
    Validate an API key for a selected LLM model.
    
    This endpoint checks whether the provided API key is valid and working
    for the specified LLM model (OpenAI, Anthropic, or Google).
    """
    try:
        return await prompt_management_service.validate_api_key(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating API key: {str(e)}")


@router.post("/submit-evaluation", response_model=PromptEvaluationResponse, status_code=201)
async def submit_evaluation(request: PromptEvaluationRequest):
    """
    Submit a prompt evaluation request.
    
    This endpoint:
    1. Receives domains and rubrics from the frontend
    2. Receives the user-entered prompt and LLM to use for evaluation
    3. Validates the selected model's API key
    4. Receives and validates test cases from the frontend
    
    The request includes:
    - domain_id: Selected domain ID
    - rubrics: List of rubrics with weights (must sum to 100%)
    - prompt: User-entered prompt to evaluate
    - llm_model: Selected LLM model (e.g., 'gpt-4', 'claude-3-opus')
    - api_key: API key for the selected LLM provider
    - test_cases: List of test cases with input and optional expected output
    """
    try:
        return await prompt_management_service.submit_evaluation(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting evaluation: {str(e)}")


@router.get("/evaluation/{evaluation_id}", response_model=PromptEvaluationRequest)
async def get_evaluation(evaluation_id: str):
    """
    Get an evaluation request by ID.
    
    Returns the full evaluation request data including domains, rubrics,
    prompt, LLM model, and test cases.
    """
    evaluation = prompt_management_service.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(
            status_code=404, 
            detail=f"Evaluation with ID '{evaluation_id}' not found"
        )
    return evaluation


@router.post("/run-evaluation/{evaluation_id}", response_model=EvaluationResultsResponse)
async def run_evaluation(evaluation_id: str):
    """
    Run evaluation for a submitted evaluation request.
    
    This endpoint:
    1. Retrieves the stored evaluation request
    2. Runs each test case with Gemini API (one by one)
    3. Generates LLM responses for each test case
    4. Compares generated outputs with expected outputs using cosine similarity
    5. Returns comprehensive evaluation results
    
    The evaluation processes test cases sequentially and provides:
    - Generated output for each test case
    - Similarity scores (when expected output is provided)
    - Overall metrics and statistics
    """
    try:
        return await prompt_management_service.run_evaluation(evaluation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running evaluation: {str(e)}")


@router.get("/evaluation-results/{evaluation_id}", response_model=EvaluationResultsResponse)
async def get_evaluation_results(evaluation_id: str):
    """
    Get evaluation results by ID.
    
    Returns the complete evaluation results including:
    - Test case results with generated outputs
    - Similarity scores and comparisons
    - Overall metrics and statistics
    """
    results = prompt_management_service.get_evaluation_results(evaluation_id)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation results for ID '{evaluation_id}' not found. Run the evaluation first."
        )
    return EvaluationResultsResponse(**results)
