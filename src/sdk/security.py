from fastapi.security import HTTPBearer
from starlette.requests import Request


class FakeHTTPBearer(HTTPBearer):
    """
    Фейковый класс для проставления в интерфейсе сваггера
    кнопки "Authorize"
    """

    async def __call__(self, request: Request) -> None:
        pass


fake_http_bearer = FakeHTTPBearer()
