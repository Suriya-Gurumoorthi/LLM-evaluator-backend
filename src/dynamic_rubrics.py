"""
Dynamic Rubrics - Constant rubrics configuration for each evaluation domain.

This module defines standard rubrics that are automatically associated with
each domain, including Reasoning, Problem Solving, Coding, Content Generation,
Information Retrieval, and other domain-specific evaluation criteria.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

import sys
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.models.rubric import (
    Rubric,
    RubricType,
    EvaluationDimension,
    RubricCriteria,
    ScoringScale
)


@dataclass
class DomainRubricConfig:
    """Configuration for rubrics associated with a domain."""
    domain_id: str
    rubrics: List[Dict]


# Standard rubric templates that can be applied across domains
STANDARD_RUBRICS = {
    "reasoning": {
        "name": "Reasoning Quality",
        "rubric_type": RubricType.REASONING,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates the logical reasoning, inference quality, and argumentation structure",
        "criteria": [
            RubricCriteria(
                name="Logical Consistency",
                description="The response demonstrates consistent logical flow without contradictions",
                weight=0.25,
                evaluation_guidelines=[
                    "Check for logical contradictions",
                    "Verify argument coherence",
                    "Assess reasoning chain validity"
                ]
            ),
            RubricCriteria(
                name="Inference Quality",
                description="The response makes appropriate inferences from given information",
                weight=0.25,
                evaluation_guidelines=[
                    "Evaluate inference validity",
                    "Check for unsupported conclusions",
                    "Assess evidence utilization"
                ]
            ),
            RubricCriteria(
                name="Argument Structure",
                description="The response presents well-structured arguments with clear premises and conclusions",
                weight=0.25,
                evaluation_guidelines=[
                    "Assess argument organization",
                    "Check premise-conclusion relationships",
                    "Evaluate argument completeness"
                ]
            ),
            RubricCriteria(
                name="Critical Thinking",
                description="The response demonstrates critical analysis and consideration of alternatives",
                weight=0.25,
                evaluation_guidelines=[
                    "Check for alternative consideration",
                    "Assess bias recognition",
                    "Evaluate analytical depth"
                ]
            )
        ],
        "instructions": "Evaluate the reasoning quality by assessing logical consistency, inference validity, argument structure, and critical thinking depth."
    },
    
    "problem_solving": {
        "name": "Problem Solving",
        "rubric_type": RubricType.ACCURACY,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates problem decomposition, solution approach, and problem-solving effectiveness",
        "criteria": [
            RubricCriteria(
                name="Problem Understanding",
                description="The response demonstrates clear understanding of the problem requirements",
                weight=0.20,
                evaluation_guidelines=[
                    "Check problem comprehension",
                    "Verify requirement identification",
                    "Assess constraint recognition"
                ]
            ),
            RubricCriteria(
                name="Solution Approach",
                description="The response presents an appropriate and effective solution strategy",
                weight=0.30,
                evaluation_guidelines=[
                    "Evaluate approach appropriateness",
                    "Check methodology selection",
                    "Assess strategy effectiveness"
                ]
            ),
            RubricCriteria(
                name="Problem Decomposition",
                description="The response breaks down complex problems into manageable components",
                weight=0.20,
                evaluation_guidelines=[
                    "Assess decomposition quality",
                    "Check sub-problem identification",
                    "Evaluate complexity management"
                ]
            ),
            RubricCriteria(
                name="Solution Correctness",
                description="The solution correctly addresses the problem and produces valid results",
                weight=0.30,
                evaluation_guidelines=[
                    "Verify solution accuracy",
                    "Check result validity",
                    "Assess completeness"
                ]
            )
        ],
        "instructions": "Evaluate problem-solving capabilities by assessing problem understanding, solution approach, decomposition quality, and solution correctness."
    },
    
    "coding_software_development": {
        "name": "Coding and Software Development",
        "rubric_type": RubricType.CODE_QUALITY,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates code quality, best practices, and software development standards",
        "criteria": [
            RubricCriteria(
                name="Syntax Correctness",
                description="The code is syntactically correct and follows language conventions",
                weight=0.20,
                evaluation_guidelines=[
                    "Check for syntax errors",
                    "Verify language conventions",
                    "Assess code structure"
                ]
            ),
            RubricCriteria(
                name="Functional Correctness",
                description="The code correctly implements the required functionality",
                weight=0.30,
                evaluation_guidelines=[
                    "Test with sample inputs",
                    "Verify edge case handling",
                    "Check output correctness"
                ]
            ),
            RubricCriteria(
                name="Code Quality",
                description="The code follows best practices, is readable, and maintainable",
                weight=0.25,
                evaluation_guidelines=[
                    "Check naming conventions",
                    "Assess code organization",
                    "Evaluate maintainability"
                ]
            ),
            RubricCriteria(
                name="Performance & Efficiency",
                description="The code demonstrates efficient algorithms and optimal resource usage",
                weight=0.15,
                evaluation_guidelines=[
                    "Assess time complexity",
                    "Check space efficiency",
                    "Evaluate optimization"
                ]
            ),
            RubricCriteria(
                name="Documentation & Comments",
                description="The code includes appropriate documentation and comments",
                weight=0.10,
                evaluation_guidelines=[
                    "Check code comments",
                    "Assess documentation quality",
                    "Evaluate clarity"
                ]
            )
        ],
        "instructions": "Evaluate code quality by assessing syntax correctness, functional correctness, code quality standards, performance, and documentation."
    },
    
    "content_generation": {
        "name": "Content Generation",
        "rubric_type": RubricType.CREATIVITY,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates content quality, creativity, engagement, and appropriateness",
        "criteria": [
            RubricCriteria(
                name="Content Quality",
                description="The content is well-written, coherent, and of high quality",
                weight=0.25,
                evaluation_guidelines=[
                    "Assess writing quality",
                    "Check coherence and flow",
                    "Evaluate language proficiency"
                ]
            ),
            RubricCriteria(
                name="Relevance & Appropriateness",
                description="The content is relevant to the request and appropriate for the context",
                weight=0.25,
                evaluation_guidelines=[
                    "Check topic relevance",
                    "Assess context appropriateness",
                    "Evaluate audience fit"
                ]
            ),
            RubricCriteria(
                name="Creativity & Originality",
                description="The content demonstrates creativity, originality, and unique perspectives",
                weight=0.20,
                evaluation_guidelines=[
                    "Assess originality",
                    "Check creative elements",
                    "Evaluate uniqueness"
                ]
            ),
            RubricCriteria(
                name="Completeness",
                description="The content fully addresses the request and provides comprehensive coverage",
                weight=0.15,
                evaluation_guidelines=[
                    "Check request fulfillment",
                    "Assess coverage completeness",
                    "Evaluate depth"
                ]
            ),
            RubricCriteria(
                name="Engagement & Clarity",
                description="The content is engaging, clear, and easy to understand",
                weight=0.15,
                evaluation_guidelines=[
                    "Assess readability",
                    "Check engagement level",
                    "Evaluate clarity"
                ]
            )
        ],
        "instructions": "Evaluate content generation by assessing quality, relevance, creativity, completeness, and engagement."
    },
    
    "information_retrieval": {
        "name": "Information Retrieval",
        "rubric_type": RubricType.RELEVANCE,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates information retrieval accuracy, relevance, and completeness",
        "criteria": [
            RubricCriteria(
                name="Relevance",
                description="The retrieved information is highly relevant to the query",
                weight=0.30,
                evaluation_guidelines=[
                    "Check query-information match",
                    "Assess topical relevance",
                    "Evaluate information appropriateness"
                ]
            ),
            RubricCriteria(
                name="Accuracy",
                description="The retrieved information is factually accurate and reliable",
                weight=0.30,
                evaluation_guidelines=[
                    "Verify factual correctness",
                    "Check source reliability",
                    "Assess information validity"
                ]
            ),
            RubricCriteria(
                name="Completeness",
                description="The retrieval covers all relevant aspects of the query",
                weight=0.20,
                evaluation_guidelines=[
                    "Check coverage breadth",
                    "Assess information depth",
                    "Evaluate comprehensiveness"
                ]
            ),
            RubricCriteria(
                name="Precision",
                description="The retrieval minimizes irrelevant information and focuses on key points",
                weight=0.20,
                evaluation_guidelines=[
                    "Check noise reduction",
                    "Assess focus quality",
                    "Evaluate precision"
                ]
            )
        ],
        "instructions": "Evaluate information retrieval by assessing relevance, accuracy, completeness, and precision of retrieved information."
    },
    
    "mathematical_correctness": {
        "name": "Mathematical Correctness",
        "rubric_type": RubricType.MATHEMATICAL_CORRECTNESS,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates mathematical accuracy, calculation correctness, and mathematical reasoning",
        "criteria": [
            RubricCriteria(
                name="Calculation Accuracy",
                description="Mathematical calculations are correct and accurate",
                weight=0.35,
                evaluation_guidelines=[
                    "Verify calculation steps",
                    "Check arithmetic accuracy",
                    "Assess computational correctness"
                ]
            ),
            RubricCriteria(
                name="Mathematical Reasoning",
                description="The mathematical reasoning and logic are sound",
                weight=0.30,
                evaluation_guidelines=[
                    "Check reasoning validity",
                    "Assess logical flow",
                    "Evaluate proof quality"
                ]
            ),
            RubricCriteria(
                name="Method Selection",
                description="Appropriate mathematical methods and techniques are selected",
                weight=0.20,
                evaluation_guidelines=[
                    "Check method appropriateness",
                    "Assess technique selection",
                    "Evaluate approach quality"
                ]
            ),
            RubricCriteria(
                name="Solution Presentation",
                description="The solution is clearly presented with proper notation and explanation",
                weight=0.15,
                evaluation_guidelines=[
                    "Check notation clarity",
                    "Assess explanation quality",
                    "Evaluate presentation"
                ]
            )
        ],
        "instructions": "Evaluate mathematical correctness by assessing calculation accuracy, reasoning quality, method selection, and solution presentation."
    },
    
    "clarity_completeness": {
        "name": "Clarity and Completeness",
        "rubric_type": RubricType.CLARITY,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates response clarity, completeness, and comprehensiveness",
        "criteria": [
            RubricCriteria(
                name="Clarity",
                description="The response is clear, well-structured, and easy to understand",
                weight=0.35,
                evaluation_guidelines=[
                    "Assess language clarity",
                    "Check structure quality",
                    "Evaluate comprehensibility"
                ]
            ),
            RubricCriteria(
                name="Completeness",
                description="The response fully addresses all aspects of the request",
                weight=0.35,
                evaluation_guidelines=[
                    "Check request fulfillment",
                    "Assess coverage breadth",
                    "Evaluate depth"
                ]
            ),
            RubricCriteria(
                name="Organization",
                description="The response is well-organized with logical flow and structure",
                weight=0.30,
                evaluation_guidelines=[
                    "Check organization quality",
                    "Assess logical flow",
                    "Evaluate structure"
                ]
            )
        ],
        "instructions": "Evaluate clarity and completeness by assessing response clarity, completeness, and organization."
    },
    
    "factual_correctness": {
        "name": "Factual Correctness",
        "rubric_type": RubricType.FACTUAL_CORRECTNESS,
        "evaluation_dimension": EvaluationDimension.RESPONSE_QUALITY,
        "description": "Evaluates factual accuracy, truthfulness, and information reliability",
        "criteria": [
            RubricCriteria(
                name="Factual Accuracy",
                description="All factual claims are accurate and verifiable",
                weight=0.40,
                evaluation_guidelines=[
                    "Verify factual claims",
                    "Check information accuracy",
                    "Assess truthfulness"
                ]
            ),
            RubricCriteria(
                name="Source Reliability",
                description="Information is drawn from reliable and credible sources",
                weight=0.30,
                evaluation_guidelines=[
                    "Check source credibility",
                    "Assess information reliability",
                    "Evaluate source quality"
                ]
            ),
            RubricCriteria(
                name="Error Avoidance",
                description="The response avoids factual errors, misconceptions, and misinformation",
                weight=0.30,
                evaluation_guidelines=[
                    "Check for errors",
                    "Assess misconception presence",
                    "Evaluate misinformation"
                ]
            )
        ],
        "instructions": "Evaluate factual correctness by assessing accuracy, source reliability, and error avoidance."
    }
}


# Domain-specific rubric mappings
DOMAIN_RUBRIC_MAPPINGS: Dict[str, List[str]] = {
    # General domains
    "domain_general_conversation": ["reasoning", "content_generation", "clarity_completeness", "factual_correctness"],
    "domain_qa_general": ["information_retrieval", "factual_correctness", "clarity_completeness", "reasoning"],
    
    # Coding domains
    "domain_python_programming": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_javascript_programming": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_java_programming": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_cpp_programming": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_sql_database": ["coding_software_development", "problem_solving", "reasoning", "information_retrieval"],
    "domain_algorithm_design": ["coding_software_development", "problem_solving", "reasoning", "mathematical_correctness"],
    "domain_code_review": ["coding_software_development", "reasoning", "clarity_completeness", "problem_solving"],
    
    # Mathematics domains
    "domain_basic_mathematics": ["mathematical_correctness", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_advanced_mathematics": ["mathematical_correctness", "problem_solving", "reasoning", "clarity_completeness"],
    "domain_statistics_probability": ["mathematical_correctness", "problem_solving", "reasoning", "information_retrieval"],
    "domain_mathematical_proofs": ["mathematical_correctness", "reasoning", "clarity_completeness", "problem_solving"],
    
    # Reasoning domains
    "domain_logical_reasoning": ["reasoning", "problem_solving", "clarity_completeness", "factual_correctness"],
    "domain_causal_reasoning": ["reasoning", "problem_solving", "clarity_completeness", "factual_correctness"],
    "domain_analytical_reasoning": ["reasoning", "problem_solving", "clarity_completeness", "information_retrieval"],
    "domain_commonsense_reasoning": ["reasoning", "factual_correctness", "clarity_completeness", "content_generation"],
    
    # Language domains
    "domain_text_summarization": ["content_generation", "information_retrieval", "clarity_completeness", "factual_correctness"],
    "domain_translation": ["content_generation", "clarity_completeness", "factual_correctness", "information_retrieval"],
    "domain_sentiment_analysis": ["information_retrieval", "reasoning", "factual_correctness", "clarity_completeness"],
    "domain_text_classification": ["information_retrieval", "reasoning", "factual_correctness", "clarity_completeness"],
    "domain_named_entity_recognition": ["information_retrieval", "factual_correctness", "clarity_completeness", "reasoning"],
    
    # Science domains
    "domain_physics": ["mathematical_correctness", "problem_solving", "reasoning", "factual_correctness"],
    "domain_chemistry": ["factual_correctness", "problem_solving", "reasoning", "mathematical_correctness"],
    "domain_biology": ["factual_correctness", "information_retrieval", "reasoning", "clarity_completeness"],
    "domain_computer_science": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    
    # Business domains
    "domain_business_analysis": ["reasoning", "problem_solving", "information_retrieval", "clarity_completeness"],
    "domain_financial_analysis": ["mathematical_correctness", "reasoning", "factual_correctness", "problem_solving"],
    "domain_marketing": ["content_generation", "reasoning", "clarity_completeness", "information_retrieval"],
    
    # Medical domains
    "domain_medical_qa": ["factual_correctness", "reasoning", "information_retrieval", "clarity_completeness"],
    "domain_clinical_reasoning": ["reasoning", "problem_solving", "factual_correctness", "information_retrieval"],
    
    # Legal domains
    "domain_legal_analysis": ["reasoning", "factual_correctness", "information_retrieval", "clarity_completeness"],
    "domain_contract_review": ["information_retrieval", "reasoning", "clarity_completeness", "factual_correctness"],
    
    # Education domains
    "domain_educational_content": ["content_generation", "clarity_completeness", "factual_correctness", "information_retrieval"],
    "domain_tutoring": ["clarity_completeness", "reasoning", "content_generation", "factual_correctness"],
    
    # Creative domains
    "domain_creative_writing": ["content_generation", "clarity_completeness", "reasoning", "creativity"],
    "domain_poetry": ["content_generation", "creativity", "clarity_completeness", "reasoning"],
    "domain_script_writing": ["content_generation", "clarity_completeness", "reasoning", "creativity"],
    
    # Technical domains
    "domain_system_design": ["problem_solving", "reasoning", "clarity_completeness", "coding_software_development"],
    "domain_api_design": ["coding_software_development", "clarity_completeness", "reasoning", "problem_solving"],
    "domain_devops": ["coding_software_development", "problem_solving", "reasoning", "clarity_completeness"],
    
    # Research domains
    "domain_research_synthesis": ["information_retrieval", "factual_correctness", "clarity_completeness", "reasoning"],
    "domain_hypothesis_generation": ["reasoning", "problem_solving", "clarity_completeness", "content_generation"],
    
    # Social domains
    "domain_social_media": ["content_generation", "clarity_completeness", "information_retrieval", "reasoning"],
    "domain_customer_service": ["content_generation", "clarity_completeness", "reasoning", "information_retrieval"],
}


def get_rubrics_for_domain(domain_id: str) -> List[Rubric]:
    """
    Get all constant rubrics for a specific domain.
    
    Args:
        domain_id: The ID of the domain
        
    Returns:
        List of Rubric objects configured for the domain
    """
    if domain_id not in DOMAIN_RUBRIC_MAPPINGS:
        # Return default rubrics if domain not found
        rubric_keys = ["reasoning", "problem_solving", "clarity_completeness"]
    else:
        rubric_keys = DOMAIN_RUBRIC_MAPPINGS[domain_id]
    
    rubrics = []
    for rubric_key in rubric_keys:
        if rubric_key in STANDARD_RUBRICS:
            rubric_config = STANDARD_RUBRICS[rubric_key]
            rubric = Rubric(
                id=f"{domain_id}_{rubric_key}",
                name=rubric_config["name"],
                rubric_type=rubric_config["rubric_type"],
                domain_id=domain_id,
                evaluation_dimension=rubric_config["evaluation_dimension"],
                description=rubric_config["description"],
                criteria=rubric_config["criteria"],
                scoring_scale=ScoringScale(),
                instructions=rubric_config["instructions"],
                metadata={"rubric_key": rubric_key, "is_standard": True}
            )
            rubrics.append(rubric)
    
    return rubrics


def get_all_standard_rubrics() -> Dict[str, Dict]:
    """Get all standard rubric templates."""
    return STANDARD_RUBRICS.copy()


def get_domain_rubric_mapping(domain_id: str) -> List[str]:
    """Get the list of rubric keys for a specific domain."""
    return DOMAIN_RUBRIC_MAPPINGS.get(domain_id, ["reasoning", "problem_solving", "clarity_completeness"])


def add_custom_rubric_to_domain(domain_id: str, rubric_key: str, rubric_config: Dict):
    """
    Add a custom rubric to a domain's rubric set.
    
    Args:
        domain_id: The domain ID
        rubric_key: Unique key for the rubric
        rubric_config: Rubric configuration dictionary
    """
    if domain_id not in DOMAIN_RUBRIC_MAPPINGS:
        DOMAIN_RUBRIC_MAPPINGS[domain_id] = []
    
    if rubric_key not in DOMAIN_RUBRIC_MAPPINGS[domain_id]:
        DOMAIN_RUBRIC_MAPPINGS[domain_id].append(rubric_key)
    
    STANDARD_RUBRICS[rubric_key] = rubric_config

