"""Service for managing prompt evaluation requests."""

import uuid
from typing import Dict, Optional
from app.schemas.prompt_management import (
    PromptEvaluationRequest,
    PromptEvaluationResponse,
    APIKeyValidationRequest,
    APIKeyValidationResponse,
    EvaluationResultsResponse
)
from app.services.llm_validator import llm_validator
from app.services.evaluation_service import evaluation_service


class PromptManagementService:
    """Service for handling prompt management operations."""
    
    def __init__(self):
        """Initialize the prompt management service."""
        self._evaluations: Dict[str, PromptEvaluationRequest] = {}
        self._evaluation_results: Dict[str, dict] = {}
    
    async def validate_api_key(
        self, 
        request: APIKeyValidationRequest
    ) -> APIKeyValidationResponse:
        """
        Validate an API key for a given LLM model.
        
        Args:
            request: APIKeyValidationRequest with model and API key
            
        Returns:
            APIKeyValidationResponse with validation result
        """
        return await llm_validator.validate_api_key(
            model_id=request.llm_model,
            api_key=request.api_key
        )
    
    async def submit_evaluation(
        self, 
        request: PromptEvaluationRequest
    ) -> PromptEvaluationResponse:
        """
        Submit a prompt evaluation request.
        
        This method:
        1. Validates the rubric weights sum to 100
        2. Validates the API key for the selected LLM
        3. Stores the evaluation request
        
        Args:
            request: PromptEvaluationRequest with all evaluation data
            
        Returns:
            PromptEvaluationResponse with success status and evaluation ID
        """
        # Validate rubric weights
        total_weight = sum(r.weight for r in request.rubrics)
        if abs(total_weight - 100.0) > 0.01:
            return PromptEvaluationResponse(
                success=False,
                message=f"Rubric weights must sum to 100%. Current total: {total_weight}%",
                evaluation_id=None
            )
        
        # Validate API key
        api_key_validation = await llm_validator.validate_api_key(
            model_id=request.llm_model,
            api_key=request.api_key
        )
        
        if not api_key_validation.is_valid:
            return PromptEvaluationResponse(
                success=False,
                message=f"API key validation failed: {api_key_validation.message}",
                evaluation_id=None
            )
        
        # Validate test cases
        if not request.test_cases or len(request.test_cases) == 0:
            return PromptEvaluationResponse(
                success=False,
                message="At least one test case is required",
                evaluation_id=None
            )
        
        # Validate that all test cases have input
        for test_case in request.test_cases:
            if not test_case.input or not test_case.input.strip():
                return PromptEvaluationResponse(
                    success=False,
                    message="All test cases must have a non-empty input",
                    evaluation_id=None
                )
        
        # Generate evaluation ID
        evaluation_id = str(uuid.uuid4())
        
        # Store the evaluation request
        self._evaluations[evaluation_id] = request
        
        return PromptEvaluationResponse(
            success=True,
            message="Evaluation request submitted successfully",
            evaluation_id=evaluation_id
        )
    
    def get_evaluation(self, evaluation_id: str) -> Optional[PromptEvaluationRequest]:
        """Get an evaluation request by ID."""
        return self._evaluations.get(evaluation_id)
    
    def list_evaluations(self) -> Dict[str, PromptEvaluationRequest]:
        """List all evaluation requests."""
        return self._evaluations.copy()
    
    async def run_evaluation(
        self,
        evaluation_id: str
    ) -> EvaluationResultsResponse:
        """
        Run evaluation for a stored evaluation request.
        
        This method:
        1. Retrieves the evaluation request
        2. Runs test cases with Gemini API
        3. Compares outputs using cosine similarity
        4. Returns comprehensive evaluation results
        
        Args:
            evaluation_id: ID of the evaluation to run
            
        Returns:
            EvaluationResultsResponse with complete results
        """
        # Get the evaluation request
        evaluation_request = self._evaluations.get(evaluation_id)
        if not evaluation_request:
            raise ValueError(f"Evaluation with ID '{evaluation_id}' not found")
        
        # Run the evaluation
        results = await evaluation_service.run_evaluation(evaluation_request)
        
        # Set the evaluation ID
        results["evaluation_id"] = evaluation_id
        
        # Store results
        self._evaluation_results[evaluation_id] = results
        
        # Convert to response schema
        return EvaluationResultsResponse(**results)
    
    def get_evaluation_results(self, evaluation_id: str) -> Optional[dict]:
        """Get evaluation results by ID."""
        return self._evaluation_results.get(evaluation_id)


# Singleton instance
prompt_management_service = PromptManagementService()
