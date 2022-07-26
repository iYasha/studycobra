from pathlib import Path
from typing import AsyncGenerator

import aiofiles
from starlette import status

from exceptions import ValidationError
from sdk.exceptions import FieldError


async def ranged(
        file,
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> AsyncGenerator[bytes, None]:
    consumed = 0

    await file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = await file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        await file.close()


async def open_file(path: Path, content_range: str) -> tuple:
    file = await aiofiles.open(path, 'rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers


def validation_error(status_code: int = status.HTTP_400_BAD_REQUEST, field: str = '',
                     message: str = '') -> ValidationError:
    return ValidationError(
        code=status_code,
        field_errors=[
            FieldError(
                field=field,
                message=message
            )
        ]
    )
