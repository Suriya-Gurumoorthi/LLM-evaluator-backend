"""Service for managing weight configurations."""

import uuid
from typing import List, Optional
from app.models.weight_config import WeightConfiguration, RubricWeight
from app.schemas.weight_config import WeightConfigCreate, WeightConfigUpdate
from app.services.rubric_service import rubric_service


class WeightConfigService:
    """Service for weight configuration management."""
    
    def __init__(self):
        """Initialize the weight config service with in-memory storage."""
        self._configs: dict[str, WeightConfiguration] = {}
        self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """Initialize with some default weight configurations."""
        # Default config for code quality focus
        code_quality_config = WeightConfiguration(
            id="weight_config_code_focus",
            name="Code Quality Focus",
            domain_id="domain_coding",
            description="Configuration emphasizing code quality metrics",
            rubric_weights={
                "rubric_code_quality": RubricWeight(
                    rubric_id="rubric_code_quality",
                    weight=0.6,
                    enabled=True
                ),
                "rubric_accuracy": RubricWeight(
                    rubric_id="rubric_accuracy",
                    weight=0.4,
                    enabled=True
                )
            },
            normalization_method="weighted_average"
        )
        
        # Default config for balanced evaluation
        balanced_config = WeightConfiguration(
            id="weight_config_balanced",
            name="Balanced Evaluation",
            domain_id=None,
            description="Balanced configuration for general evaluation",
            rubric_weights={
                "rubric_accuracy": RubricWeight(
                    rubric_id="rubric_accuracy",
                    weight=0.5,
                    enabled=True
                ),
                "rubric_reasoning": RubricWeight(
                    rubric_id="rubric_reasoning",
                    weight=0.5,
                    enabled=True
                )
            },
            normalization_method="weighted_average"
        )
        
        self._configs[code_quality_config.id] = code_quality_config
        self._configs[balanced_config.id] = balanced_config
    
    def create_weight_config(self, config_data: WeightConfigCreate) -> WeightConfiguration:
        """Create a new weight configuration."""
        config_id = config_data.id or f"weight_config_{uuid.uuid4().hex[:8]}"
        
        if config_id in self._configs:
            raise ValueError(f"Weight configuration with ID '{config_id}' already exists")
        
        # Validate that all referenced rubrics exist
        self._validate_rubrics(config_data.rubric_weights)
        
        config = WeightConfiguration(
            id=config_id,
            **config_data.model_dump(exclude={'id'})
        )
        
        self._configs[config_id] = config
        return config
    
    def _validate_rubrics(self, rubric_weights: dict[str, RubricWeight]):
        """Validate that all referenced rubrics exist."""
        for rubric_id, rubric_weight in rubric_weights.items():
            if rubric_weight.enabled:
                rubric = rubric_service.get_rubric(rubric_id)
                if not rubric:
                    raise ValueError(f"Rubric with ID '{rubric_id}' not found")
    
    def get_weight_config(self, config_id: str) -> Optional[WeightConfiguration]:
        """Get a weight configuration by ID."""
        return self._configs.get(config_id)
    
    def get_all_configs(self, domain_id: Optional[str] = None) -> List[WeightConfiguration]:
        """Get all weight configurations, optionally filtered by domain."""
        configs = list(self._configs.values())
        
        if domain_id:
            configs = [c for c in configs if c.domain_id == domain_id]
        
        return configs
    
    def update_weight_config(
        self,
        config_id: str,
        config_update: WeightConfigUpdate
    ) -> WeightConfiguration:
        """Update an existing weight configuration."""
        config = self.get_weight_config(config_id)
        if not config:
            raise ValueError(f"Weight configuration with ID '{config_id}' not found")
        
        update_data = config_update.model_dump(exclude_unset=True)
        
        # Validate rubrics if rubric_weights are being updated
        if 'rubric_weights' in update_data:
            self._validate_rubrics(update_data['rubric_weights'])
        
        updated_config = config.model_copy(update=update_data)
        
        self._configs[config_id] = updated_config
        return updated_config
    
    def delete_weight_config(self, config_id: str) -> bool:
        """Delete a weight configuration."""
        if config_id not in self._configs:
            return False
        
        del self._configs[config_id]
        return True
    
    def get_configs_by_domain(self, domain_id: str) -> List[WeightConfiguration]:
        """Get all weight configurations for a specific domain."""
        return self.get_all_configs(domain_id=domain_id)
    
    def create_config_from_rubrics(
        self,
        name: str,
        rubric_ids: List[str],
        weights: Optional[List[float]] = None,
        domain_id: Optional[str] = None,
        normalization_method: str = "weighted_average"
    ) -> WeightConfiguration:
        """Helper method to create a weight configuration from a list of rubric IDs."""
        if weights is None:
            # Equal weights if not specified
            weight_value = 1.0 / len(rubric_ids) if rubric_ids else 1.0
            weights = [weight_value] * len(rubric_ids)
        
        if len(rubric_ids) != len(weights):
            raise ValueError("Number of rubric IDs must match number of weights")
        
        rubric_weights = {
            rubric_id: RubricWeight(
                rubric_id=rubric_id,
                weight=weight,
                enabled=True
            )
            for rubric_id, weight in zip(rubric_ids, weights)
        }
        
        config_data = WeightConfigCreate(
            name=name,
            domain_id=domain_id,
            rubric_weights=rubric_weights,
            normalization_method=normalization_method
        )
        
        return self.create_weight_config(config_data)


# Global service instance
weight_config_service = WeightConfigService()

