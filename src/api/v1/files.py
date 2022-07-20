from uuid import UUID

import aiofiles
from fastapi import APIRouter, UploadFile, File, Header
from fastapi import status
from pathlib import Path
from starlette.responses import StreamingResponse, FileResponse
from pydantic.error_wrappers import ValidationError as SchemaValidationError

import enums
import models
import schemas
from core.config import settings
from exceptions.schemas import ExceptionModel

from sdk import utils

router = APIRouter()


@router.get(
    "/{file_id}",
)
async def get_file(
    *,
    file_id: UUID,
    content_range: str = Header(None, alias='Range'),
):
    """ Получить файл """

    file_obj = await models.File.get(uuid=file_id)
    if not file_obj:
        raise utils.validation_error(status_code=status.HTTP_404_NOT_FOUND, field='file_id', message='Файл не найден')
    file_path = settings.MEDIA_DIR + str(file_obj.uuid)
    if file_obj.content_type == enums.FileType.MP4_VIDEO:
        file, status_code, content_length, headers = await utils.open_file(Path(file_path), content_range)
        response = StreamingResponse(
            file,
            media_type=file_obj.content_type,
            status_code=status_code,
        )

        response.headers.update(
            {
                'Accept-Ranges': 'bytes',
                'Content-Length': str(content_length),
                **headers,
            }
        )
        return response
    return FileResponse(
        path=file_path,
        media_type=file_obj.content_type
    )


@router.post(
    '/',
)
async def upload_file(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),  # noqa
    file: UploadFile = File(...),
) -> schemas.File:
    """ Загрузить файл """
    content = await file.read()
    mb_size = round(len(content) / 1024 ** 2, 2)
    if mb_size > settings.MAX_FILE_UPLOAD_SIZE_MB:
        raise utils.validation_error(
            field='file',
            message=f'Размер файла не должен превышать {settings.MAX_FILE_UPLOAD_SIZE_MB} MB'
        )
    try:
        new_file = schemas.CreateFile(
            name=file.filename,
            content_type=file.content_type,
            size=mb_size,
        )
    except SchemaValidationError:
        raise utils.validation_error(
            field='content_type',
            message=f'Неверный формат файла, допустимые форматы: {", ".join(enums.FileType.__members__.values())}'
        )
    file_obj = await models.File.create(**new_file.dict())
    async with aiofiles.open(settings.MEDIA_DIR + str(file_obj.uuid), 'wb') as out_file:
        await out_file.write(content)
    return file_obj
