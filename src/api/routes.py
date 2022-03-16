from api.v1 import healthchecks
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(healthchecks.router, prefix="/healthchecks", tags=["healthchecks"])
