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
    '/',
    response_model=List[schemas.Group],
    responses={},
)
async def get_all_groups(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    is_archived: bool = Query(...)
) -> List[schemas.Group]:
    """Получить все группы"""

    groups = await models.Group.filter(is_archived=is_archived).all().select_related('course').prefetch_related('teachers', 'students', 'teachers__user')
    return schemas.Group.from_queryset(groups)


@router.get(
    '/{group_id}',
    response_model=schemas.GroupDetail,
    responses={},
)
async def get_all_groups(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID
) -> schemas.GroupDetail:
    """Получить конкретную группу"""

    group = await models.Group.get(uuid=group_id).select_related('course').prefetch_related('teachers', 'students', 'students__user', 'teachers__user')
    return schemas.GroupDetail.from_orm(group)


@router.post(
    '/',
    response_model=schemas.Group,
    responses={},
)
@atomic()
async def create_group(
    *,
    user: models.User = Depends(deps.get_current_user),
    new_group: schemas.GroupCreate
) -> schemas.Group:
    """Создать группу"""

    return await services.GroupService.create_group(user, new_group)


@router.put(
    '/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    group_data: schemas.GroupUpdate
) -> Response:
    """Обновить данные группы"""

    group = await models.Group.get(uuid=group_id)
    await group.update_from_dict(group_data.dict())
    await group.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID
) -> Response:
    """Удалить группу"""

    await models.Group.filter(uuid=group_id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
