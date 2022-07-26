from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from fastapi import status
from starlette.responses import Response
from tortoise.transactions import atomic

import models
import schemas
from api import deps

router = APIRouter()


@router.get(
    '/{group_id}/students',
    response_model=List[schemas.GroupStudent],
)
async def get_students(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID
) -> List[schemas.GroupStudent]:
    """Получить список студентов"""

    return schemas.GroupStudent.from_queryset(
        await models.GroupStudent.filter(group_id=group_id).prefetch_related('user')
    )


@router.post(
    '/{group_id}/students/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
@atomic()
async def add_student_to_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    is_archived: bool = Body(..., embed=True),
    group_id: UUID,
    user_id: UUID
):
    """Добавить/обновить студента в группе"""

    await models.GroupStudent.update_or_create(
        user_id=user_id,
        group_id=group_id,
        defaults={'is_archived': is_archived}
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    '/{group_id}/students/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_student_from_group(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    group_id: UUID,
    user_id: UUID
):
    """Удалить студента из группы"""

    await models.GroupStudent.filter(user_id=user_id, group_id=group_id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
