from api.v1 import healthchecks, authorizations
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(healthchecks.router, prefix="/healthcheck", tags=["healthchecks"])
api_router.include_router(authorizations.router, prefix="/oauth", tags=["oauth"])
