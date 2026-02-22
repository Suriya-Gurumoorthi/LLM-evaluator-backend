"""
Domain Selector - Comprehensive list of evaluation domains for LLM evaluation.

This module provides a curated list of domains that users can select from
for evaluating LLM performance across different contexts and use cases.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class DomainCategory(str, Enum):
    """Domain categories for classification."""
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
    RESEARCH = "research"
    SOCIAL = "social"
    CUSTOM = "custom"


@dataclass
class Domain:
    """Domain representation for selection."""
    id: str
    name: str
    category: DomainCategory
    description: str
    metadata: Optional[Dict] = None


# Comprehensive list of evaluation domains
AVAILABLE_DOMAINS: List[Domain] = [
    # General & Conversational Domains
    Domain(
        id="domain_general_conversation",
        name="General Conversation",
        category=DomainCategory.GENERAL,
        description="Evaluation of general conversational abilities, context understanding, and natural dialogue",
        metadata={"complexity": "medium", "use_cases": ["chatbots", "assistants", "customer_service"]}
    ),
    Domain(
        id="domain_qa_general",
        name="General Question Answering",
        category=DomainCategory.GENERAL,
        description="Evaluation of factual question answering across diverse topics",
        metadata={"complexity": "low", "use_cases": ["search", "knowledge_base", "information_retrieval"]}
    ),
    
    # Coding & Software Development Domains
    Domain(
        id="domain_python_programming",
        name="Python Programming",
        category=DomainCategory.CODING,
        description="Evaluation of Python code generation, debugging, and software development tasks",
        metadata={"language": "python", "complexity": "high", "use_cases": ["code_generation", "debugging", "refactoring"]}
    ),
    Domain(
        id="domain_javascript_programming",
        name="JavaScript Programming",
        category=DomainCategory.CODING,
        description="Evaluation of JavaScript/TypeScript code generation for web and Node.js applications",
        metadata={"language": "javascript", "complexity": "high", "use_cases": ["web_development", "frontend", "backend"]}
    ),
    Domain(
        id="domain_java_programming",
        name="Java Programming",
        category=DomainCategory.CODING,
        description="Evaluation of Java code generation for enterprise and Android applications",
        metadata={"language": "java", "complexity": "high", "use_cases": ["enterprise", "android", "backend"]}
    ),
    Domain(
        id="domain_cpp_programming",
        name="C++ Programming",
        category=DomainCategory.CODING,
        description="Evaluation of C++ code generation for system programming and performance-critical applications",
        metadata={"language": "cpp", "complexity": "very_high", "use_cases": ["systems", "gaming", "embedded"]}
    ),
    Domain(
        id="domain_sql_database",
        name="SQL & Database Queries",
        category=DomainCategory.CODING,
        description="Evaluation of SQL query generation, optimization, and database design",
        metadata={"language": "sql", "complexity": "medium", "use_cases": ["data_analysis", "backend", "reporting"]}
    ),
    Domain(
        id="domain_algorithm_design",
        name="Algorithm Design & Analysis",
        category=DomainCategory.CODING,
        description="Evaluation of algorithm design, complexity analysis, and optimization",
        metadata={"complexity": "very_high", "use_cases": ["competitive_programming", "research", "optimization"]}
    ),
    Domain(
        id="domain_code_review",
        name="Code Review & Refactoring",
        category=DomainCategory.CODING,
        description="Evaluation of code review capabilities, bug detection, and refactoring suggestions",
        metadata={"complexity": "high", "use_cases": ["quality_assurance", "maintenance", "best_practices"]}
    ),
    
    # Mathematics Domains
    Domain(
        id="domain_basic_mathematics",
        name="Basic Mathematics",
        category=DomainCategory.MATHEMATICS,
        description="Evaluation of arithmetic, algebra, and basic mathematical problem solving",
        metadata={"level": "basic", "complexity": "low", "use_cases": ["education", "calculations"]}
    ),
    Domain(
        id="domain_advanced_mathematics",
        name="Advanced Mathematics",
        category=DomainCategory.MATHEMATICS,
        description="Evaluation of calculus, linear algebra, differential equations, and advanced mathematical concepts",
        metadata={"level": "advanced", "complexity": "very_high", "use_cases": ["research", "engineering", "academia"]}
    ),
    Domain(
        id="domain_statistics_probability",
        name="Statistics & Probability",
        category=DomainCategory.MATHEMATICS,
        description="Evaluation of statistical analysis, probability theory, and data interpretation",
        metadata={"complexity": "high", "use_cases": ["data_science", "research", "analytics"]}
    ),
    Domain(
        id="domain_mathematical_proofs",
        name="Mathematical Proofs",
        category=DomainCategory.MATHEMATICS,
        description="Evaluation of mathematical proof construction and logical reasoning",
        metadata={"complexity": "very_high", "use_cases": ["academia", "research", "theoretical_math"]}
    ),
    
    # Reasoning Domains
    Domain(
        id="domain_logical_reasoning",
        name="Logical Reasoning",
        category=DomainCategory.REASONING,
        description="Evaluation of deductive and inductive reasoning, logical inference, and argument analysis",
        metadata={"complexity": "high", "use_cases": ["critical_thinking", "analysis", "decision_making"]}
    ),
    Domain(
        id="domain_causal_reasoning",
        name="Causal Reasoning",
        category=DomainCategory.REASONING,
        description="Evaluation of cause-and-effect understanding, causal chains, and counterfactual reasoning",
        metadata={"complexity": "high", "use_cases": ["explanation", "diagnosis", "planning"]}
    ),
    Domain(
        id="domain_analytical_reasoning",
        name="Analytical Reasoning",
        category=DomainCategory.REASONING,
        description="Evaluation of complex problem decomposition, pattern recognition, and analytical thinking",
        metadata={"complexity": "very_high", "use_cases": ["problem_solving", "strategy", "analysis"]}
    ),
    Domain(
        id="domain_commonsense_reasoning",
        name="Commonsense Reasoning",
        category=DomainCategory.REASONING,
        description="Evaluation of everyday knowledge, social understanding, and commonsense inference",
        metadata={"complexity": "medium", "use_cases": ["nlp", "conversation", "understanding"]}
    ),
    
    # Language & NLP Domains
    Domain(
        id="domain_text_summarization",
        name="Text Summarization",
        category=DomainCategory.LANGUAGE,
        description="Evaluation of extractive and abstractive text summarization capabilities",
        metadata={"complexity": "medium", "use_cases": ["content_creation", "research", "news"]}
    ),
    Domain(
        id="domain_translation",
        name="Translation",
        category=DomainCategory.LANGUAGE,
        description="Evaluation of machine translation quality across different language pairs",
        metadata={"complexity": "high", "use_cases": ["localization", "communication", "content"]}
    ),
    Domain(
        id="domain_sentiment_analysis",
        name="Sentiment Analysis",
        category=DomainCategory.LANGUAGE,
        description="Evaluation of emotion detection, sentiment classification, and tone analysis",
        metadata={"complexity": "medium", "use_cases": ["social_media", "customer_feedback", "market_research"]}
    ),
    Domain(
        id="domain_text_classification",
        name="Text Classification",
        category=DomainCategory.LANGUAGE,
        description="Evaluation of topic classification, intent detection, and text categorization",
        metadata={"complexity": "medium", "use_cases": ["content_moderation", "routing", "organization"]}
    ),
    Domain(
        id="domain_named_entity_recognition",
        name="Named Entity Recognition",
        category=DomainCategory.LANGUAGE,
        description="Evaluation of entity extraction, relationship identification, and information extraction",
        metadata={"complexity": "medium", "use_cases": ["knowledge_graphs", "search", "data_extraction"]}
    ),
    
    # Science Domains
    Domain(
        id="domain_physics",
        name="Physics",
        category=DomainCategory.SCIENCE,
        description="Evaluation of physics problem solving, concept understanding, and scientific reasoning",
        metadata={"complexity": "high", "use_cases": ["education", "research", "engineering"]}
    ),
    Domain(
        id="domain_chemistry",
        name="Chemistry",
        category=DomainCategory.SCIENCE,
        description="Evaluation of chemical reactions, molecular understanding, and chemistry problem solving",
        metadata={"complexity": "high", "use_cases": ["education", "research", "pharmaceuticals"]}
    ),
    Domain(
        id="domain_biology",
        name="Biology",
        category=DomainCategory.SCIENCE,
        description="Evaluation of biological concepts, processes, and scientific knowledge",
        metadata={"complexity": "medium", "use_cases": ["education", "research", "medical"]}
    ),
    Domain(
        id="domain_computer_science",
        name="Computer Science Theory",
        category=DomainCategory.SCIENCE,
        description="Evaluation of CS theory, data structures, computer architecture, and systems design",
        metadata={"complexity": "very_high", "use_cases": ["academia", "research", "system_design"]}
    ),
    
    # Business Domains
    Domain(
        id="domain_business_analysis",
        name="Business Analysis",
        category=DomainCategory.BUSINESS,
        description="Evaluation of business strategy, market analysis, and decision-making frameworks",
        metadata={"complexity": "high", "use_cases": ["consulting", "strategy", "planning"]}
    ),
    Domain(
        id="domain_financial_analysis",
        name="Financial Analysis",
        category=DomainCategory.BUSINESS,
        description="Evaluation of financial modeling, risk assessment, and economic analysis",
        metadata={"complexity": "high", "use_cases": ["finance", "investment", "accounting"]}
    ),
    Domain(
        id="domain_marketing",
        name="Marketing & Advertising",
        category=DomainCategory.BUSINESS,
        description="Evaluation of marketing strategy, content creation, and campaign planning",
        metadata={"complexity": "medium", "use_cases": ["advertising", "content", "strategy"]}
    ),
    
    # Medical Domains
    Domain(
        id="domain_medical_qa",
        name="Medical Question Answering",
        category=DomainCategory.MEDICAL,
        description="Evaluation of medical knowledge, diagnosis support, and healthcare information",
        metadata={"complexity": "very_high", "use_cases": ["healthcare", "education", "research"], "warning": "Not for actual medical diagnosis"}
    ),
    Domain(
        id="domain_clinical_reasoning",
        name="Clinical Reasoning",
        category=DomainCategory.MEDICAL,
        description="Evaluation of clinical decision-making, symptom analysis, and treatment planning",
        metadata={"complexity": "very_high", "use_cases": ["education", "training", "research"], "warning": "Educational purposes only"}
    ),
    
    # Legal Domains
    Domain(
        id="domain_legal_analysis",
        name="Legal Analysis",
        category=DomainCategory.LEGAL,
        description="Evaluation of legal reasoning, case analysis, and contract interpretation",
        metadata={"complexity": "very_high", "use_cases": ["research", "education", "analysis"], "warning": "Not legal advice"}
    ),
    Domain(
        id="domain_contract_review",
        name="Contract Review",
        category=DomainCategory.LEGAL,
        description="Evaluation of contract analysis, clause identification, and risk assessment",
        metadata={"complexity": "very_high", "use_cases": ["compliance", "review", "analysis"], "warning": "Requires professional review"}
    ),
    
    # Education Domains
    Domain(
        id="domain_educational_content",
        name="Educational Content Creation",
        category=DomainCategory.EDUCATION,
        description="Evaluation of lesson planning, educational material generation, and pedagogical content",
        metadata={"complexity": "medium", "use_cases": ["teaching", "curriculum", "learning"]}
    ),
    Domain(
        id="domain_tutoring",
        name="Tutoring & Explanation",
        category=DomainCategory.EDUCATION,
        description="Evaluation of explanatory capabilities, step-by-step instruction, and concept clarification",
        metadata={"complexity": "medium", "use_cases": ["learning", "support", "guidance"]}
    ),
    
    # Creative Domains
    Domain(
        id="domain_creative_writing",
        name="Creative Writing",
        category=DomainCategory.CREATIVE,
        description="Evaluation of storytelling, narrative generation, and creative content creation",
        metadata={"complexity": "medium", "use_cases": ["content", "entertainment", "art"]}
    ),
    Domain(
        id="domain_poetry",
        name="Poetry & Literary Arts",
        category=DomainCategory.CREATIVE,
        description="Evaluation of poetic composition, literary style, and artistic expression",
        metadata={"complexity": "medium", "use_cases": ["art", "entertainment", "expression"]}
    ),
    Domain(
        id="domain_script_writing",
        name="Script & Screenplay Writing",
        category=DomainCategory.CREATIVE,
        description="Evaluation of script generation, dialogue writing, and screenplay formatting",
        metadata={"complexity": "high", "use_cases": ["entertainment", "media", "content"]}
    ),
    
    # Technical Domains
    Domain(
        id="domain_system_design",
        name="System Design",
        category=DomainCategory.TECHNICAL,
        description="Evaluation of architecture design, scalability planning, and technical system solutions",
        metadata={"complexity": "very_high", "use_cases": ["engineering", "architecture", "planning"]}
    ),
    Domain(
        id="domain_api_design",
        name="API Design & Documentation",
        category=DomainCategory.TECHNICAL,
        description="Evaluation of API design, documentation quality, and developer experience",
        metadata={"complexity": "high", "use_cases": ["development", "integration", "documentation"]}
    ),
    Domain(
        id="domain_devops",
        name="DevOps & Infrastructure",
        category=DomainCategory.TECHNICAL,
        description="Evaluation of infrastructure as code, CI/CD pipelines, and deployment strategies",
        metadata={"complexity": "high", "use_cases": ["operations", "automation", "deployment"]}
    ),
    
    # Research Domains
    Domain(
        id="domain_research_synthesis",
        name="Research Synthesis",
        category=DomainCategory.RESEARCH,
        description="Evaluation of literature review, research summarization, and academic writing",
        metadata={"complexity": "very_high", "use_cases": ["academia", "research", "publication"]}
    ),
    Domain(
        id="domain_hypothesis_generation",
        name="Hypothesis Generation",
        category=DomainCategory.RESEARCH,
        description="Evaluation of research question formulation, hypothesis development, and experimental design",
        metadata={"complexity": "very_high", "use_cases": ["research", "academia", "innovation"]}
    ),
    
    # Social Domains
    Domain(
        id="domain_social_media",
        name="Social Media Content",
        category=DomainCategory.SOCIAL,
        description="Evaluation of social media post generation, engagement optimization, and platform-specific content",
        metadata={"complexity": "low", "use_cases": ["marketing", "engagement", "content"]}
    ),
    Domain(
        id="domain_customer_service",
        name="Customer Service",
        category=DomainCategory.SOCIAL,
        description="Evaluation of customer interaction, problem resolution, and service quality",
        metadata={"complexity": "medium", "use_cases": ["support", "satisfaction", "retention"]}
    ),
]


def get_all_domains() -> List[Domain]:
    """Get all available domains for selection."""
    return AVAILABLE_DOMAINS.copy()


def get_domain_by_id(domain_id: str) -> Optional[Domain]:
    """Get a specific domain by its ID."""
    for domain in AVAILABLE_DOMAINS:
        if domain.id == domain_id:
            return domain
    return None


def get_domains_by_category(category: DomainCategory) -> List[Domain]:
    """Get all domains in a specific category."""
    return [domain for domain in AVAILABLE_DOMAINS if domain.category == category]


def get_domain_names() -> List[str]:
    """Get a list of all domain names."""
    return [domain.name for domain in AVAILABLE_DOMAINS]


def search_domains(query: str) -> List[Domain]:
    """Search domains by name or description."""
    query_lower = query.lower()
    return [
        domain for domain in AVAILABLE_DOMAINS
        if query_lower in domain.name.lower() or query_lower in domain.description.lower()
    ]


def get_domain_categories() -> List[str]:
    """Get all available domain categories."""
    return [category.value for category in DomainCategory]

