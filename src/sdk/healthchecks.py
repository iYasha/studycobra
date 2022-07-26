import os
import uuid
from asyncio import get_event_loop

import aio_pika
import aiofiles
import psutil
from aio_pika import RobustConnection
from tortoise.transactions import in_transaction

from core.config import settings

SUCCESS_STATUS = "working"
DISK_USAGE_MAX = 90  # percentage
MEMORY_MIN = 100  # Mb


async def check_database() -> str:
    query = "SELECT 1"
    try:
        async with in_transaction() as tconn:
            await tconn.execute_query(query)
    except Exception as e:
        return str(e)
    return SUCCESS_STATUS


async def check_rabbitmq() -> str:
    loop = get_event_loop()
    try:
        connection: RobustConnection = await aio_pika.connect_robust(settings.RABBIT_URL, loop=loop)
        await connection.close()
    except Exception as e:
        return repr(e)
    return SUCCESS_STATUS


def check_memory_usage() -> str:
    memory = psutil.virtual_memory()
    if MEMORY_MIN and memory.available < (MEMORY_MIN * 1024 * 1024):
        avail = "{:n}".format(int(memory.available / 1024 / 1024))
        threshold = "{:n}".format(MEMORY_MIN)
        return "{avail} MB available RAM below {threshold} MB".format(
            avail=avail,
            threshold=threshold,
        )
    return SUCCESS_STATUS


def check_disk_usage() -> str:
    du = psutil.disk_usage("/")
    if DISK_USAGE_MAX and du.percent >= DISK_USAGE_MAX:
        return "{percent}% disk usage exceeds {disk_usage}%".format(
            percent=du.percent,
            disk_usage=DISK_USAGE_MAX,
        )
    return SUCCESS_STATUS


async def check_file_storage() -> str:
    file_name = "test-%s.txt" % uuid.uuid4()
    content = "this is the healthtest file content"

    try:
        async with aiofiles.open(file_name, mode="w") as f:
            await f.write(content)

        if not os.path.exists(file_name):
            raise Exception("File not exist")

        async with aiofiles.open(file_name, mode="r") as f:
            result = await f.read()

        if result != content:
            raise Exception("File content does not match")

        os.remove(file_name)

    except Exception as e:
        return str(e)

    return SUCCESS_STATUS
