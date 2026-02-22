"""Weight configuration model for rubric consolidation."""

from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator


class RubricWeight(BaseModel):
    """Weight configuration for a single rubric."""
    rubric_id: str = Field(..., description="ID of the rubric")
    weight: float = Field(..., description="Weight value (0.0 to 1.0)", ge=0.0, le=1.0)
    enabled: bool = Field(True, description="Whether this rubric is enabled")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rubric_id": "rubric_001",
                "weight": 0.4,
                "enabled": True
            }
        }


class WeightConfiguration(BaseModel):
    """Configuration for consolidating multiple rubrics with weights."""
    
    id: Optional[str] = Field(None, description="Unique identifier for the weight configuration")
    name: str = Field(..., description="Configuration name", min_length=1, max_length=100)
    domain_id: Optional[str] = Field(None, description="Associated domain ID")
    description: Optional[str] = Field(None, description="Configuration description", max_length=500)
    rubric_weights: Dict[str, RubricWeight] = Field(
        ...,
        description="Dictionary mapping rubric IDs to their weights",
        min_length=1
    )
    normalization_method: str = Field(
        "weighted_average",
        description="Method for normalizing scores: 'weighted_average', 'weighted_sum', 'max', 'min'"
    )
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")
    
    @field_validator('normalization_method')
    @classmethod
    def validate_normalization_method(cls, v):
        allowed_methods = ['weighted_average', 'weighted_sum', 'max', 'min', 'geometric_mean']
        if v not in allowed_methods:
            raise ValueError(f"normalization_method must be one of {allowed_methods}")
        return v
    
    @field_validator('rubric_weights')
    @classmethod
    def validate_weights(cls, v):
        """Validate that weights are properly configured."""
        if not v:
            raise ValueError("At least one rubric weight must be specified")
        
        # Check that enabled rubrics have non-zero weights
        enabled_weights = [rw.weight for rw in v.values() if rw.enabled]
        if not enabled_weights:
            raise ValueError("At least one rubric must be enabled")
        
        return v
    
    def get_total_weight(self) -> float:
        """Calculate total weight of enabled rubrics."""
        return sum(rw.weight for rw in self.rubric_weights.values() if rw.enabled)
    
    def normalize_weights(self) -> Dict[str, float]:
        """Normalize weights so they sum to 1.0."""
        total = self.get_total_weight()
        if total == 0:
            return {}
        return {
            rubric_id: rw.weight / total
            for rubric_id, rw in self.rubric_weights.items()
            if rw.enabled
        }
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "weight_config_001",
                "name": "Code Quality Focus",
                "domain_id": "domain_001",
                "description": "Configuration emphasizing code quality metrics",
                "rubric_weights": {
                    "rubric_001": {
                        "rubric_id": "rubric_001",
                        "weight": 0.5,
                        "enabled": True
                    },
                    "rubric_002": {
                        "rubric_id": "rubric_002",
                        "weight": 0.3,
                        "enabled": True
                    },
                    "rubric_003": {
                        "rubric_id": "rubric_003",
                        "weight": 0.2,
                        "enabled": True
                    }
                },
                "normalization_method": "weighted_average",
                "metadata": {}
            }
        }

