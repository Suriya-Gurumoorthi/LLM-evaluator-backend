"""API routes for rubric management."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.rubric import RubricType, EvaluationDimension
from app.schemas.rubric import RubricCreate, RubricUpdate, RubricResponse
from app.services.rubric_service import rubric_service

router = APIRouter()


@router.post("", response_model=RubricResponse, status_code=201)
async def create_rubric(rubric: RubricCreate):
    """Create a new rubric."""
    try:
        return rubric_service.create_rubric(rubric)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[RubricResponse])
async def get_rubrics(
    domain_id: Optional[str] = Query(None, description="Filter by domain ID"),
    rubric_type: Optional[RubricType] = Query(None, description="Filter by rubric type"),
    evaluation_dimension: Optional[EvaluationDimension] = Query(
        None, description="Filter by evaluation dimension"
    )
):
    """Get all rubrics with optional filters."""
    return rubric_service.get_all_rubrics(
        domain_id=domain_id,
        rubric_type=rubric_type,
        evaluation_dimension=evaluation_dimension
    )


@router.get("/{rubric_id}", response_model=RubricResponse)
async def get_rubric(rubric_id: str):
    """Get a rubric by ID."""
    rubric = rubric_service.get_rubric(rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail=f"Rubric with ID '{rubric_id}' not found")
    return rubric


@router.put("/{rubric_id}", response_model=RubricResponse)
async def update_rubric(rubric_id: str, rubric_update: RubricUpdate):
    """Update an existing rubric."""
    try:
        return rubric_service.update_rubric(rubric_id, rubric_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{rubric_id}", status_code=204)
async def delete_rubric(rubric_id: str):
    """Delete a rubric."""
    if not rubric_service.delete_rubric(rubric_id):
        raise HTTPException(status_code=404, detail=f"Rubric with ID '{rubric_id}' not found")
    return None


@router.get("/domain/{domain_id}", response_model=List[RubricResponse])
async def get_rubrics_by_domain(domain_id: str):
    """Get all rubrics for a specific domain."""
    return rubric_service.get_rubrics_by_domain(domain_id)


@router.get("/types/list", response_model=List[str])
async def get_rubric_types():
    """Get all available rubric types."""
    return rubric_service.get_rubric_types()


@router.post("/build-custom", response_model=RubricResponse, status_code=201)
async def build_custom_rubric(
    name: str,
    rubric_type: RubricType,
    criteria: List[dict],
    domain_id: Optional[str] = None,
    evaluation_dimension: EvaluationDimension = EvaluationDimension.RESPONSE_QUALITY
):
    """Build a custom rubric from criteria."""
    try:
        return rubric_service.build_custom_rubric(
            name=name,
            rubric_type=rubric_type,
            criteria=criteria,
            domain_id=domain_id,
            evaluation_dimension=evaluation_dimension
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

