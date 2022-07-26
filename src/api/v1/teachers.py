from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from fastapi import status
from starlette.responses import Response

import enums
import models
import schemas
from api import deps

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

