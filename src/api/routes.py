from api.v1 import healthchecks, authorizations, groups, files
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(healthchecks.router, prefix="/healthcheck", tags=["healthchecks"])
api_router.include_router(authorizations.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
