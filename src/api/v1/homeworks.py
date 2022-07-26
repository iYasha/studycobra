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


@router.post(
    '/{group_id}/lessons/{lesson_id}/homeworks',
    response_model=schemas.Homework,
    responses={},
)
@atomic()
async def create_homework(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    lesson_id: UUID,
    new_homework: schemas.HomeworkCreate
) -> schemas.Homework:
    """Создать домашнее задание"""

    author = None
    if new_homework.author_id is not None:
        author = await models.GroupTeacher.get(uuid=new_homework.author_id).prefetch_related('user')

    homework = await models.Homework.create(lesson_id=lesson_id, author=author, **new_homework.dict(exclude={'author', 'additional_files', 'quiz'}))

    additional_files = await models.File.filter(uuid__in=new_homework.additional_files)

    quizzes = []
    if homework.homework_type == enums.HomeworkType.QUIZ:
        quizzes = await services.QuizService.create_quizzes(homework_id=homework.uuid, new_quizzes=new_homework.quiz)

    await homework.additional_files.add(*additional_files)

    await homework.save()

    return schemas.Homework(author=author, quizzes=quizzes, additional_files=additional_files, **dict(homework))


@router.get(
    '/{group_id}/lessons/{lesson_id}/homeworks',
    response_model=List[schemas.Homework],
    responses={},
)
async def get_homeworks(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    lesson_id: UUID,
) -> List[schemas.Homework]:
    """Получить список домашних заданий"""

    homeworks = await models.Homework.filter(lesson_id=lesson_id).order_by('created_at').select_related('author').prefetch_related('additional_files')

    return schemas.Homework.from_queryset(homeworks)


@router.get(
    '/{group_id}/homeworks/{homework_id}',
    response_model=schemas.Homework,
    responses={},
)
async def get_homework(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    homework_id: UUID,
) -> schemas.Homework:
    """Получить подробную информацию о домашнем задании"""

    homework = await models.Homework.get(uuid=homework_id).select_related('author').prefetch_related('additional_files', 'quizzes', 'quizzes__answers', 'author__user')
    return schemas.Homework.from_orm(homework)


@router.put(
    '/{group_id}/homeworks/{homework_id}',
    response_model=schemas.Homework,
)
@atomic()
async def update_homework(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    homework_id: UUID,
    updated_homework: schemas.HomeworkCreate
) -> schemas.Homework:
    """Обновить информацию о домашнем задании"""

    additional_files = await models.File.filter(uuid__in=updated_homework.additional_files)

    author = None
    if updated_homework.author_id is not None:
        author = await models.GroupTeacher.get(uuid=updated_homework.author_id).prefetch_related('user')

    homework = await models.Homework.get(uuid=homework_id)

    for field in updated_homework.dict(exclude={'author', 'additional_files'}):
        setattr(homework, field, updated_homework.dict()[field])

    homework.author = author

    await homework.additional_files.clear()
    await homework.additional_files.add(*additional_files)

    quizzes = []
    if homework.homework_type == enums.HomeworkType.QUIZ:
        await homework.quizzes.all().delete()
        quizzes = await services.QuizService.create_quizzes(homework_id=homework.uuid, new_quizzes=updated_homework.quizzes)

    await homework.save()

    return schemas.Homework(author=author, quizzes=quizzes, additional_files=additional_files, **dict(homework))
