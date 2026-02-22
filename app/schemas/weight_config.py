"""API schemas for Weight Configuration operations."""

from typing import Optional, Dict
from pydantic import BaseModel
from app.models.weight_config import WeightConfiguration, RubricWeight


class WeightConfigCreate(WeightConfiguration):
    """Schema for creating a new weight configuration."""
    pass


class WeightConfigUpdate(BaseModel):
    """Schema for updating a weight configuration."""
    name: Optional[str] = None
    domain_id: Optional[str] = None
    description: Optional[str] = None
    rubric_weights: Optional[Dict[str, RubricWeight]] = None
    normalization_method: Optional[str] = None
    metadata: Optional[dict] = None


class WeightConfigResponse(WeightConfiguration):
    """Schema for weight configuration response."""
    normalized_weights: Optional[Dict[str, float]] = None
    
    @classmethod
    def from_config(cls, config: WeightConfiguration):
        """Create response with normalized weights."""
        return cls(
            **config.model_dump(),
            normalized_weights=config.normalize_weights()
        )



