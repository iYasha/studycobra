from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestWidget(TestBase):

    def test_unauthorized_user_cant_see_widgets(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/widgets')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_widget_ok(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        # Authorize as guest
        access_token = self.get_access_token(client)

        # Get widgets
        response = client.get(
            self.get_url('/widgets'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(widget.get('language') for widget in response_data) == {'ru'}
        self.assert_keys(response_data[0].keys(),
                         ('language', 'id', 'widget_type', 'cover_type', 'title', 'text_color', 'background_color',
                          'index', 'is_active', 'file_id', 'file', 'collection_id', 'books', 'book_id', 'book',
                          'background_for_ipad'))

    def test_widget_other_language(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        # Authorize as guest
        access_token = self.get_access_token(client)

        # Get widgets
        response = client.get(
            self.get_url('/widgets'),
            headers=self.get_authorization_header(access_token, language='aa')
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data == []
