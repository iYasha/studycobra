from datetime import timedelta
from typing import List, Union
from uuid import UUID

from starlette.responses import Response
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

import enums
from core import security
from core.config import settings
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from fastapi import status

from exceptions import ValidationError
from exceptions.schemas import ExceptionModel
import schemas
import models
from sdk.exceptions import FieldError
from api import deps
import services

router = APIRouter()


@router.get(
    '/{group_id}/lessons',
    response_model=List[schemas.Lesson],
    responses={},
)
async def get_lessons(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID
) -> List[schemas.Lesson]:
    """Получить список занятий"""

    lessons = await models.Lesson.filter(group_id=group_id).order_by('start_at')
    return schemas.Lesson.from_queryset(lessons)


@router.get(
    '/{group_id}/lessons/{lesson_id}',
    response_model=schemas.LessonDetail,
    responses={},
)
async def get_lesson(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    lesson_id: UUID
) -> schemas.LessonDetail:
    """Получить подробную информацию о занятии"""

    lesson = await models.Lesson.get(uuid=lesson_id).prefetch_related('additional_files', 'teachers', 'teachers__user')
    return schemas.LessonDetail.from_orm(lesson)


@router.post(
    '/{group_id}/lessons',
    response_model=schemas.LessonDetail,
    responses={},
)
@atomic()
async def create_lesson(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    new_lesson: schemas.LessonCreate
) -> schemas.LessonDetail:
    """Создать занятие"""

    lesson = await models.Lesson.create(group_id=group_id, **new_lesson.dict(exclude={'teachers', 'additional_files'}))

    teachers = await models.GroupTeacher.filter(uuid__in=new_lesson.teachers).prefetch_related('user')
    additional_files = await models.File.filter(uuid__in=new_lesson.additional_files)

    await lesson.teachers.add(*teachers)
    await lesson.additional_files.add(*additional_files)

    await lesson.save()

    return schemas.LessonDetail(teachers=teachers, additional_files=additional_files, **dict(lesson))


@router.patch(
    '/{group_id}/lessons/{lesson_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def partly_update_lesson(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    lesson_id: UUID,
    updated_lesson: schemas.LessonPartlyUpdate
) -> Response:
    """Частично обновить информацию о занятии"""

    additional_files = await models.File.filter(uuid__in=updated_lesson.additional_files)

    lesson = await models.Lesson.get(uuid=lesson_id)
    lesson.title = updated_lesson.title
    lesson.description = updated_lesson.description

    await lesson.additional_files.clear()
    await lesson.additional_files.add(*additional_files)

    await lesson.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    '/{group_id}/lessons/{lesson_id}',
    response_model=schemas.LessonDetail,
)
async def update_lesson(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    lesson_id: UUID,
    updated_lesson: schemas.LessonCreate
) -> schemas.LessonDetail:
    """Обновить информацию о занятии"""

    teachers = await models.GroupTeacher.filter(uuid__in=updated_lesson.teachers).prefetch_related('user')
    additional_files = await models.File.filter(uuid__in=updated_lesson.additional_files)

    lesson = await models.Lesson.get(uuid=lesson_id)

    for field in updated_lesson.dict(exclude={'teachers', 'additional_files'}):
        setattr(lesson, field, updated_lesson.dict()[field])

    await lesson.teachers.clear()
    await lesson.teachers.add(*teachers)

    await lesson.additional_files.clear()
    await lesson.additional_files.add(*additional_files)

    await lesson.save()

    return schemas.LessonDetail(teachers=teachers, additional_files=additional_files, **dict(lesson))

