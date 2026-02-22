"""Service for managing domains."""

import uuid
from typing import List, Optional
from app.models.domain import Domain, DomainCategory
from app.schemas.domain import DomainCreate, DomainUpdate


class DomainService:
    """Service for domain selection and management."""
    
    def __init__(self):
        """Initialize the domain service with in-memory storage."""
        self._domains: dict[str, Domain] = {}
        self._initialize_default_domains()
    
    def _initialize_default_domains(self):
        """Initialize with some default domains."""
        default_domains = [
            Domain(
                id="domain_general",
                name="General Purpose",
                category=DomainCategory.GENERAL,
                description="General purpose LLM evaluation",
                metadata={}
            ),
            Domain(
                id="domain_coding",
                name="Code Generation",
                category=DomainCategory.CODING,
                description="Evaluation for code generation tasks",
                metadata={"languages": ["python", "javascript", "java", "cpp"]}
            ),
            Domain(
                id="domain_math",
                name="Mathematics",
                category=DomainCategory.MATHEMATICS,
                description="Mathematical problem solving evaluation",
                metadata={"levels": ["basic", "intermediate", "advanced"]}
            ),
            Domain(
                id="domain_reasoning",
                name="Reasoning",
                category=DomainCategory.REASONING,
                description="Logical reasoning and problem solving",
                metadata={}
            ),
        ]
        
        for domain in default_domains:
            self._domains[domain.id] = domain
    
    def create_domain(self, domain_data: DomainCreate) -> Domain:
        """Create a new domain."""
        domain_id = domain_data.id or f"domain_{uuid.uuid4().hex[:8]}"
        
        if domain_id in self._domains:
            raise ValueError(f"Domain with ID '{domain_id}' already exists")
        
        domain = Domain(
            id=domain_id,
            **domain_data.model_dump(exclude={'id'})
        )
        
        self._domains[domain_id] = domain
        return domain
    
    def get_domain(self, domain_id: str) -> Optional[Domain]:
        """Get a domain by ID."""
        return self._domains.get(domain_id)
    
    def get_all_domains(self, category: Optional[DomainCategory] = None) -> List[Domain]:
        """Get all domains, optionally filtered by category."""
        domains = list(self._domains.values())
        
        if category:
            domains = [d for d in domains if d.category == category]
        
        return domains
    
    def update_domain(self, domain_id: str, domain_update: DomainUpdate) -> Domain:
        """Update an existing domain."""
        domain = self.get_domain(domain_id)
        if not domain:
            raise ValueError(f"Domain with ID '{domain_id}' not found")
        
        update_data = domain_update.model_dump(exclude_unset=True)
        updated_domain = domain.model_copy(update=update_data)
        
        self._domains[domain_id] = updated_domain
        return updated_domain
    
    def delete_domain(self, domain_id: str) -> bool:
        """Delete a domain."""
        if domain_id not in self._domains:
            return False
        
        del self._domains[domain_id]
        return True
    
    def search_domains(self, query: str) -> List[Domain]:
        """Search domains by name or description."""
        query_lower = query.lower()
        return [
            domain for domain in self._domains.values()
            if query_lower in domain.name.lower() or
            (domain.description and query_lower in domain.description.lower())
        ]


# Global service instance
domain_service = DomainService()

