from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestFiles(TestBase):
    file_id = '52fd6a77-792d-489f-9eef-a38a6cd292e2'

    def test_get_files(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url(f'/files/{self.file_id}')
        )
        assert response.status_code == status.HTTP_200_OK
