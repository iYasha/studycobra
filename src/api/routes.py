from api.v1 import healthchecks, authorizations, groups, files, lessons, students, teachers, homeworks, homework_answers
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(healthchecks.router, prefix="/healthcheck", tags=["healthchecks"])
api_router.include_router(authorizations.router, prefix="/oauth", tags=["oauth"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(students.router, prefix="/groups", tags=["students"])
api_router.include_router(teachers.router, prefix="/groups", tags=["teachers"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(lessons.router, prefix="/groups", tags=["lessons"])
api_router.include_router(homeworks.router, prefix="/groups", tags=["homeworks"])
api_router.include_router(homework_answers.router, prefix="/homeworks", tags=["homeworks"])
