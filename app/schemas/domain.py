"""API schemas for Domain operations."""

from typing import Optional
from pydantic import BaseModel
from app.models.domain import Domain, DomainCategory


class DomainCreate(Domain):
    """Schema for creating a new domain."""
    pass


class DomainUpdate(BaseModel):
    """Schema for updating a domain."""
    name: Optional[str] = None
    category: Optional[DomainCategory] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


class DomainResponse(Domain):
    """Schema for domain response."""
    pass

