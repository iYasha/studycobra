from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from starlette.responses import Response
from tortoise.transactions import atomic

import enums
import models
import schemas
from api import deps
from exceptions.schemas import ExceptionModel
from sdk.utils import validation_error

router = APIRouter()


@router.get(
    '/{homework_id}/answer',
    response_model=List[schemas.HomeworkAnswer],
)
async def get_homework_answers(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    homework_id: UUID
) -> List[schemas.HomeworkAnswer]:

    return schemas.HomeworkAnswer.from_queryset(
        await models.HomeworkAnswer.filter(homework_id=homework_id).prefetch_related('file', 'teacher_file', 'student')
    )


@router.post(
    '/{homework_id}/answer',
    response_model=schemas.HomeworkAnswer,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": 'Нельзя сдать домашку',
            "model": ExceptionModel,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": 'Server Error',
            "model": ExceptionModel,
        },
    },
)
@atomic()
async def create_homework_answer(
    *,
    user: models.User = Depends(deps.get_current_user),  # noqa
    homework_id: UUID,
    new_answer: schemas.HomeworkAnswerStudentCreate
) -> schemas.HomeworkAnswer:
    """
    Отправка решения от студента
    """

    homework = await models.Homework.get(uuid=homework_id)
    retakes_count = await models.HomeworkAnswer.filter(
        student_id=user.uuid,
        homework_id=homework_id
    ).count()
    last_answer = await models.HomeworkAnswer.filter(
        student_id=user.uuid,
        homework_id=homework_id,
        points=None
    ).first()

    if not homework.can_be_created(retakes_count):
        raise validation_error(
            status_code=status.HTTP_403_FORBIDDEN,
            message='Время сдачи истекло или вы превысили лимит попыток'
        )

    if last_answer:
        raise validation_error(status_code=status.HTTP_403_FORBIDDEN, message='Вы уже отправили решение на проверку')

    answer = await models.HomeworkAnswer.create(
        homework_id=homework_id,
        student_id=user.uuid,
        answer=new_answer.answer,
        file_id=new_answer.file_id,
    )
    return schemas.HomeworkAnswer.from_orm(
        await models.HomeworkAnswer.get(uuid=answer.uuid).prefetch_related('file', 'student')
    )


@router.put(
    '/{homework_id}/answer/{answer_id}',
    response_model=schemas.HomeworkAnswer,
)
@atomic()
async def update_homework_answer(
    *,
    user: models.User = Depends(deps.get_current_user),  # noqa
    answer_id: UUID,
    update_answer: schemas.HomeworkAnswerTeacherCreate
) -> schemas.HomeworkAnswer:
    """
    Ответ преподавателя на решение
    """

    await models.HomeworkAnswer.filter(uuid=answer_id).update(
        points=update_answer.points,
        description=update_answer.teacher_description,
        teacher_file_id=update_answer.teacher_file_id,
    )

    return schemas.HomeworkAnswer.from_orm(
        await models.HomeworkAnswer.get(uuid=answer_id).prefetch_related('file', 'teacher_file', 'student')
    )


@router.delete(
    '/{homework_id}/answer/{answer_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": 'Нельзя удалить решение',
            "model": ExceptionModel,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": 'Server Error',
            "model": ExceptionModel,
        },
    },
)
async def delete_homework_answer(
    *,
    user: models.User = Depends(deps.get_current_user),  # noqa
    answer_id: UUID,
) -> Response:
    answer = await models.HomeworkAnswer.get(uuid=answer_id)

    if user.role == enums.UserRole.STUDENT and answer.points is not None:
        raise validation_error(status_code=status.HTTP_403_FORBIDDEN, message='Нельзя удалить проверенное решение')

    await answer.delete()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
