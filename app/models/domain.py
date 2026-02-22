"""Domain model for categorizing evaluation contexts."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DomainCategory(str, Enum):
    """Predefined domain categories."""
    GENERAL = "general"
    CODING = "coding"
    MATHEMATICS = "mathematics"
    REASONING = "reasoning"
    LANGUAGE = "language"
    SCIENCE = "science"
    BUSINESS = "business"
    MEDICAL = "medical"
    LEGAL = "legal"
    EDUCATION = "education"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    CUSTOM = "custom"


class Domain(BaseModel):
    """Domain model representing an evaluation domain."""
    
    id: Optional[str] = Field(None, description="Unique identifier for the domain")
    name: str = Field(..., description="Domain name", min_length=1, max_length=100)
    category: DomainCategory = Field(..., description="Domain category")
    description: Optional[str] = Field(None, description="Domain description", max_length=500)
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "domain_001",
                "name": "Python Programming",
                "category": "coding",
                "description": "Evaluation domain for Python code generation and analysis",
                "metadata": {
                    "language": "python",
                    "version": "3.11"
                }
            }
        }

