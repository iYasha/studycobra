from core.celery_app import celery_app
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from schemas.healthchecks import HealthCheckStatuses
from sdk import healthchecks as hc_utils
from starlette.responses import PlainTextResponse

router = APIRouter()


@router.get("/readiness", response_class=PlainTextResponse)
def readiness() -> str:
    """ Простейший эндпоинт для проверки работоспособности сервиса """
    return "Ok"


@router.get("/celery", response_class=PlainTextResponse)
def readiness() -> str:
    """ Простейший эндпоинт для проверки работоспособности Celery Worker """
    task = celery_app.send_task('test_celery', args=['hello'], queue="main-queue", routing_key='main-queue')
    return str(task)


# @router.get("/check_database", response_class=PlainTextResponse)
# async def check_database() -> str:
#     """ Эндпоинт для проверки коннекта к БД """
#
#     query = "SELECT 1"
#     result = await database.execute(query)
#     return str(result)


@router.get("/sentry_debug")
def sentry_debug() -> None:
    """ Простейший эндпоинт для проверки работоспособности отправки ошибок в Sentry """

    raise Exception


@router.get(
    "/liveness",
    response_model=HealthCheckStatuses,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Validation Error",
            "model": HealthCheckStatuses,
        }
    },
)
async def liveness() -> JSONResponse:
    """ Сводная информация по работоспособности различных компонентов, используемых сервисом """

    status_code = status.HTTP_200_OK
    hc_statuses = HealthCheckStatuses(
        DatabaseBackend=await hc_utils.check_database(),
        DefaultFileStorageHealthCheck=await hc_utils.check_file_storage(),
        DiskUsage=hc_utils.check_disk_usage(),
        MemoryUsage=hc_utils.check_memory_usage(),
        RabbitMQHealthCheck=await hc_utils.check_rabbitmq(),
    )

    if not hc_statuses.is_all_success():
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(content=hc_statuses.dict(), status_code=status_code)
