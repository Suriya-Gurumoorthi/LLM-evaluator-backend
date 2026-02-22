"""API routes for weight configuration management."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.weight_config import (
    WeightConfigCreate,
    WeightConfigUpdate,
    WeightConfigResponse
)
from app.services.weight_config_service import weight_config_service

router = APIRouter()


@router.post("", response_model=WeightConfigResponse, status_code=201)
async def create_weight_config(config: WeightConfigCreate):
    """Create a new weight configuration."""
    try:
        created_config = weight_config_service.create_weight_config(config)
        return WeightConfigResponse.from_config(created_config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[WeightConfigResponse])
async def get_weight_configs(
    domain_id: Optional[str] = Query(None, description="Filter by domain ID")
):
    """Get all weight configurations, optionally filtered by domain."""
    configs = weight_config_service.get_all_configs(domain_id=domain_id)
    return [WeightConfigResponse.from_config(config) for config in configs]


@router.get("/{config_id}", response_model=WeightConfigResponse)
async def get_weight_config(config_id: str):
    """Get a weight configuration by ID."""
    config = weight_config_service.get_weight_config(config_id)
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Weight configuration with ID '{config_id}' not found"
        )
    return WeightConfigResponse.from_config(config)


@router.put("/{config_id}", response_model=WeightConfigResponse)
async def update_weight_config(config_id: str, config_update: WeightConfigUpdate):
    """Update an existing weight configuration."""
    try:
        updated_config = weight_config_service.update_weight_config(config_id, config_update)
        return WeightConfigResponse.from_config(updated_config)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{config_id}", status_code=204)
async def delete_weight_config(config_id: str):
    """Delete a weight configuration."""
    if not weight_config_service.delete_weight_config(config_id):
        raise HTTPException(
            status_code=404,
            detail=f"Weight configuration with ID '{config_id}' not found"
        )
    return None


@router.get("/domain/{domain_id}", response_model=List[WeightConfigResponse])
async def get_weight_configs_by_domain(domain_id: str):
    """Get all weight configurations for a specific domain."""
    configs = weight_config_service.get_configs_by_domain(domain_id)
    return [WeightConfigResponse.from_config(config) for config in configs]


@router.post("/from-rubrics", response_model=WeightConfigResponse, status_code=201)
async def create_config_from_rubrics(
    name: str,
    rubric_ids: List[str],
    weights: Optional[List[float]] = None,
    domain_id: Optional[str] = None,
    normalization_method: str = "weighted_average"
):
    """Create a weight configuration from a list of rubric IDs."""
    try:
        config = weight_config_service.create_config_from_rubrics(
            name=name,
            rubric_ids=rubric_ids,
            weights=weights,
            domain_id=domain_id,
            normalization_method=normalization_method
        )
        return WeightConfigResponse.from_config(config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



