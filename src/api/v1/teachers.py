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
    '/{group_id}/teachers',
    response_model=List[schemas.GroupTeacher],
)
async def get_teachers(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID
) -> List[schemas.GroupTeacher]:
    """Получить список преподавателей"""

    return schemas.GroupTeacher.from_queryset(
        await models.GroupTeacher.filter(group_id=group_id).prefetch_related('user')
    )


@router.post(
    '/{group_id}/teachers/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_teacher_to_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    role: enums.TeacherRole = Body(..., embed=True),
    group_id: UUID,
    user_id: UUID
):
    """Добавить/обновить преподавателя в группе"""

    await models.GroupTeacher.update_or_create(user_id=user_id, group_id=group_id, defaults={'role': role})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/{group_id}/teachers/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_teacher_from_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    user_id: UUID
):
    """Удалить преподавателя из группы"""

    await models.GroupTeacher.filter(user_id=user_id, group_id=group_id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

