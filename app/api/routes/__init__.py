from fastapi import APIRouter
from .domain import router as domain_router
from .rubric import router as rubric_router
from .weight_config import router as weight_config_router
from .prompt_management import router as prompt_management_router

api_router = APIRouter()

api_router.include_router(domain_router, prefix="/domains", tags=["domains"])
api_router.include_router(rubric_router, prefix="/rubrics", tags=["rubrics"])
api_router.include_router(weight_config_router, prefix="/weight-configs", tags=["weight-configs"])
api_router.include_router(prompt_management_router, prefix="/prompt-management", tags=["prompt-management"])



