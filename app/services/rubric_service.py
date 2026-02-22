"""Service for managing dynamic rubrics."""

import uuid
from typing import List, Optional
from app.models.rubric import Rubric, RubricType, EvaluationDimension
from app.schemas.rubric import RubricCreate, RubricUpdate


class RubricService:
    """Service for dynamic rubric building and management."""
    
    def __init__(self):
        """Initialize the rubric service with in-memory storage."""
        self._rubrics: dict[str, Rubric] = {}
        self._initialize_default_rubrics()
    
    def _initialize_default_rubrics(self):
        """Initialize with some default rubrics."""
        from app.models.rubric import RubricCriteria, ScoringScale
        
        default_rubrics = [
            Rubric(
                id="rubric_code_quality",
                name="Code Quality",
                rubric_type=RubricType.CODE_QUALITY,
                domain_id="domain_coding",
                evaluation_dimension=EvaluationDimension.RESPONSE_QUALITY,
                description="Evaluates code quality including correctness, style, and best practices",
                criteria=[
                    RubricCriteria(
                        name="Syntax Correctness",
                        description="Code must be syntactically correct and executable",
                        weight=0.3,
                        evaluation_guidelines=["Check for syntax errors", "Verify imports are correct"]
                    ),
                    RubricCriteria(
                        name="Logical Correctness",
                        description="Code must solve the problem correctly",
                        weight=0.4,
                        evaluation_guidelines=["Test with sample inputs", "Check edge cases"]
                    ),
                    RubricCriteria(
                        name="Code Style",
                        description="Code should follow best practices and style guidelines",
                        weight=0.3,
                        evaluation_guidelines=["Check naming conventions", "Verify documentation"]
                    )
                ],
                scoring_scale=ScoringScale(min_score=0.0, max_score=10.0, step=0.1),
                instructions="Evaluate the code based on syntax correctness, logical correctness, and code style."
            ),
            Rubric(
                id="rubric_reasoning",
                name="Reasoning Ability",
                rubric_type=RubricType.REASONING,
                domain_id="domain_reasoning",
                evaluation_dimension=EvaluationDimension.RESPONSE_QUALITY,
                description="Evaluates logical reasoning and problem-solving ability",
                criteria=[
                    RubricCriteria(
                        name="Logical Coherence",
                        description="Arguments and steps must be logically coherent",
                        weight=0.4,
                        evaluation_guidelines=["Check logical flow", "Verify step-by-step reasoning"]
                    ),
                    RubricCriteria(
                        name="Problem Analysis",
                        description="Ability to correctly analyze and break down problems",
                        weight=0.3,
                        evaluation_guidelines=["Check problem understanding", "Verify approach"]
                    ),
                    RubricCriteria(
                        name="Solution Quality",
                        description="Quality and correctness of the solution",
                        weight=0.3,
                        evaluation_guidelines=["Verify solution correctness", "Check completeness"]
                    )
                ],
                scoring_scale=ScoringScale(min_score=0.0, max_score=10.0, step=0.1),
                instructions="Evaluate the reasoning process and solution quality."
            ),
            Rubric(
                id="rubric_accuracy",
                name="Accuracy",
                rubric_type=RubricType.ACCURACY,
                domain_id=None,
                evaluation_dimension=EvaluationDimension.RESPONSE_QUALITY,
                description="Evaluates factual accuracy and correctness",
                criteria=[
                    RubricCriteria(
                        name="Factual Correctness",
                        description="Information must be factually correct",
                        weight=0.5,
                        evaluation_guidelines=["Verify facts", "Check against reference materials"]
                    ),
                    RubricCriteria(
                        name="Completeness",
                        description="Response should be complete and comprehensive",
                        weight=0.3,
                        evaluation_guidelines=["Check if all aspects are covered"]
                    ),
                    RubricCriteria(
                        name="Relevance",
                        description="Response should be relevant to the query",
                        weight=0.2,
                        evaluation_guidelines=["Check relevance to the question"]
                    )
                ],
                scoring_scale=ScoringScale(min_score=0.0, max_score=10.0, step=0.1),
                instructions="Evaluate the accuracy, completeness, and relevance of the response."
            )
        ]
        
        for rubric in default_rubrics:
            self._rubrics[rubric.id] = rubric
    
    def create_rubric(self, rubric_data: RubricCreate) -> Rubric:
        """Create a new rubric."""
        rubric_id = rubric_data.id or f"rubric_{uuid.uuid4().hex[:8]}"
        
        if rubric_id in self._rubrics:
            raise ValueError(f"Rubric with ID '{rubric_id}' already exists")
        
        rubric = Rubric(
            id=rubric_id,
            **rubric_data.model_dump(exclude={'id'})
        )
        
        self._rubrics[rubric_id] = rubric
        return rubric
    
    def get_rubric(self, rubric_id: str) -> Optional[Rubric]:
        """Get a rubric by ID."""
        return self._rubrics.get(rubric_id)
    
    def get_all_rubrics(
        self,
        domain_id: Optional[str] = None,
        rubric_type: Optional[RubricType] = None,
        evaluation_dimension: Optional[EvaluationDimension] = None
    ) -> List[Rubric]:
        """Get all rubrics with optional filters."""
        rubrics = list(self._rubrics.values())
        
        if domain_id:
            rubrics = [r for r in rubrics if r.domain_id == domain_id]
        
        if rubric_type:
            rubrics = [r for r in rubrics if r.rubric_type == rubric_type]
        
        if evaluation_dimension:
            rubrics = [r for r in rubrics if r.evaluation_dimension == evaluation_dimension]
        
        return rubrics
    
    def update_rubric(self, rubric_id: str, rubric_update: RubricUpdate) -> Rubric:
        """Update an existing rubric."""
        rubric = self.get_rubric(rubric_id)
        if not rubric:
            raise ValueError(f"Rubric with ID '{rubric_id}' not found")
        
        update_data = rubric_update.model_dump(exclude_unset=True)
        updated_rubric = rubric.model_copy(update=update_data)
        
        self._rubrics[rubric_id] = updated_rubric
        return updated_rubric
    
    def delete_rubric(self, rubric_id: str) -> bool:
        """Delete a rubric."""
        if rubric_id not in self._rubrics:
            return False
        
        del self._rubrics[rubric_id]
        return True
    
    def get_rubrics_by_domain(self, domain_id: str) -> List[Rubric]:
        """Get all rubrics for a specific domain."""
        return self.get_all_rubrics(domain_id=domain_id)
    
    def get_rubric_types(self) -> List[str]:
        """Get all available rubric types."""
        return [rt.value for rt in RubricType]
    
    def build_custom_rubric(
        self,
        name: str,
        rubric_type: RubricType,
        criteria: List[dict],
        domain_id: Optional[str] = None,
        evaluation_dimension: EvaluationDimension = EvaluationDimension.RESPONSE_QUALITY
    ) -> Rubric:
        """Helper method to build a custom rubric from criteria."""
        from app.models.rubric import RubricCriteria
        
        rubric_criteria = [
            RubricCriteria(**c) if isinstance(c, dict) else c
            for c in criteria
        ]
        
        rubric_data = RubricCreate(
            name=name,
            rubric_type=rubric_type,
            domain_id=domain_id,
            evaluation_dimension=evaluation_dimension,
            criteria=rubric_criteria
        )
        
        return self.create_rubric(rubric_data)


# Global service instance
rubric_service = RubricService()

