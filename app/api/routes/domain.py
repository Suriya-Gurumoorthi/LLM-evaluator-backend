"""API routes for domain management."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.domain import DomainCategory
from app.schemas.domain import DomainCreate, DomainUpdate, DomainResponse
from app.services.domain_service import domain_service

router = APIRouter()


@router.post("", response_model=DomainResponse, status_code=201)
async def create_domain(domain: DomainCreate):
    """Create a new domain."""
    try:
        return domain_service.create_domain(domain)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[DomainResponse])
async def get_domains(
    category: Optional[DomainCategory] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name or description")
):
    """Get all domains, optionally filtered by category or search query."""
    if search:
        return domain_service.search_domains(search)
    return domain_service.get_all_domains(category=category)


@router.get("/{domain_id}", response_model=DomainResponse)
async def get_domain(domain_id: str):
    """Get a domain by ID."""
    domain = domain_service.get_domain(domain_id)
    if not domain:
        raise HTTPException(status_code=404, detail=f"Domain with ID '{domain_id}' not found")
    return domain


@router.put("/{domain_id}", response_model=DomainResponse)
async def update_domain(domain_id: str, domain_update: DomainUpdate):
    """Update an existing domain."""
    try:
        return domain_service.update_domain(domain_id, domain_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{domain_id}", status_code=204)
async def delete_domain(domain_id: str):
    """Delete a domain."""
    if not domain_service.delete_domain(domain_id):
        raise HTTPException(status_code=404, detail=f"Domain with ID '{domain_id}' not found")
    return None


@router.get("/categories/list", response_model=List[str])
async def get_domain_categories():
    """Get all available domain categories."""
    return [category.value for category in DomainCategory]

