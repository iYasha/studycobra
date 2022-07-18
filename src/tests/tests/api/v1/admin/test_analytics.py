import datetime

from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAnalytics(TestBase):
    """Тесты для проверки работоспособности АПИ аналитики"""

    def test_get_analytic_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/search/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('page_count', 'next', 'previous', 'total_count', 'results'))
        self.assert_keys(response_data.get('results')[0].keys(), ('search_name', 'count', 'localization'))

    def test_get_analytic_search_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/search/'),
            params={'q': 'Fai'},
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data.get('results')[0].get('search_name') == 'Fai'

    def test_get_analytic_search_with_filter(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/search/'),
            params={
                'localization': ['en']
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('localization') for data in response_data.get('results')]) == {'English'}

        self.get_async_result(crud.SearchCRUD.update(obj_id='adedde22-a59d-4488-823c-12e29fc1fdc0',
                                                     created_at=datetime.datetime(2022, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/search/'),
            params={
                'created_at_before': '2022-05-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('search_name') for data in response_data.get('results')]) == {'Fai'}

        self.get_async_result(crud.SearchCRUD.update(obj_id='adedde22-a59d-4488-823c-12e29fc1fdc0',
                                                     created_at=datetime.datetime(2023, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/search/'),
            params={
                'created_at_after': '2023-04-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('search_name') for data in response_data.get('results')]) == {'Fai'}

    def test_get_search_excel(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/search/export/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_ratings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('page_count', 'next', 'previous', 'total_count', 'results'))
        self.assert_keys(response_data.get('results')[0].keys(),
                         ('id', 'admin_id', 'name', 'authors', 'publisher_title', 'book_type',
                          'localization', 'like', 'dislike', 'avg_rating',
                          'nr_rating'))

    def test_get_ratings_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            params={'q': 'Покорители'},
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data.get('results')[0].get('name') == 'Покорители Глубин. История подводных погружений'

    def test_get_rating_excel(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/ratings/export/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_ratings_with_filter(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        # Localizations filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            params={
                'localization': ['ru']
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('localization') for data in response_data.get('results')]) == {'Russian'}

        # Created_at_before filter
        self.get_async_result(crud.BookCRUD.update(obj_id='f4afa085-601c-4157-9c89-9ae069eeffed',
                                                   created_at=datetime.datetime(2021, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            params={
                'created_at_before': '2021-05-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('name') for data in response_data.get('results')]) == {
            'Покорители Глубин. История подводных погружений'}

        # Created_at_after filter
        self.get_async_result(crud.BookCRUD.update(obj_id='f4afa085-601c-4157-9c89-9ae069eeffed',
                                                   created_at=datetime.datetime(2023, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            params={
                'created_at_after': '2023-04-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('name') for data in response_data.get('results')]) == {
            'Покорители Глубин. История подводных погружений'}

        # Book types filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'book_types': 'time_code'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([book.get('book_type') for book in response_data.get('results')]) == {'Single audio'}

        # Publisher filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'publisher_id': ['315e66f5-d4e2-4eba-8a4e-70ec049e27a5']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        publisher = self.get_async_result(crud.PublisherCRUD.get_one(id='315e66f5-d4e2-4eba-8a4e-70ec049e27a5'))
        assert set([book.get('publisher_title') for book in response_data.get('results')]) == {publisher.name}

        # Category filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'category_ids': ['675cc7a4-4197-49e5-abf9-1216325fefda']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_categories = self.get_async_result(crud.BookCategoryCRUD.get_all(book_id=book_id))
                assert '675cc7a4-4197-49e5-abf9-1216325fefda' in [str(book_category.category_id) for book_category in
                                                                  book_categories]

        # Author filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'author_ids': ['2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_authors = self.get_async_result(crud.BookAuthorCRUD.get_all(book_id=book_id))
                assert '2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9' in [str(book_author.author_id) for book_author in
                                                                  book_authors]

        # Series filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'series_ids': ['5a539a6f-5415-4cc6-8473-3f17d28cc071']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_series = self.get_async_result(crud.BookSeriesCRUD.get_all(book_id=book_id))
                assert '5a539a6f-5415-4cc6-8473-3f17d28cc071' in [str(book_seria.series_id) for book_seria in
                                                                  book_series]

        # Tag filter
        response = client.get(
            self.get_admin_url('/analytics/ratings/'),
            headers=self.get_authorization_header(access_token),
            params={'tag_ids': ['096af069-a0e8-4ede-8edc-2a029691abef']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_tags = self.get_async_result(crud.BookTagCRUD.get_all(book_id=book_id))
                assert '096af069-a0e8-4ede-8edc-2a029691abef' in [str(book_tag.tag_id) for book_tag in book_tags]

    def test_get_read(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('page_count', 'next', 'previous', 'total_count', 'results'))
        self.assert_keys(response_data.get('results')[0].keys(),
                         ('id', 'admin_id', 'name', 'authors', 'publisher_title', 'book_type',
                          'localization', 'total_pages_read', 'book_read_count'))

    def test_get_read_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            params={'q': 'Покорители'},
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data.get('results')[0].get('name') == 'Покорители Глубин. История подводных погружений'

    def test_get_read_excel(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/analytics/read/export/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_read_with_filter(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        # Localizations filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            params={
                'localization': ['ru']
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('localization') for data in response_data.get('results')]) == {'Russian'}

        # Created_at_before filter
        self.get_async_result(crud.BookCRUD.update(obj_id='f4afa085-601c-4157-9c89-9ae069eeffed',
                                                   created_at=datetime.datetime(2021, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            params={
                'created_at_before': '2021-05-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('name') for data in response_data.get('results')]) == {
            'Покорители Глубин. История подводных погружений'}

        # Created_at_after filter
        self.get_async_result(crud.BookCRUD.update(obj_id='f4afa085-601c-4157-9c89-9ae069eeffed',
                                                   created_at=datetime.datetime(2023, 5, 28, 15, 00, 10, 137334)))
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            params={
                'created_at_after': '2023-04-29 15:00:00'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([data.get('name') for data in response_data.get('results')]) == {
            'Покорители Глубин. История подводных погружений'}

        # Book types filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'book_types': 'time_code'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set([book.get('book_type') for book in response_data.get('results')]) == {'Single audio'}

        # Publisher filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'publisher_id': ['315e66f5-d4e2-4eba-8a4e-70ec049e27a5']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        publisher = self.get_async_result(crud.PublisherCRUD.get_one(id='315e66f5-d4e2-4eba-8a4e-70ec049e27a5'))
        assert set([book.get('publisher_title') for book in response_data.get('results')]) == {publisher.name}

        # Category filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'category_ids': ['675cc7a4-4197-49e5-abf9-1216325fefda']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_categories = self.get_async_result(crud.BookCategoryCRUD.get_all(book_id=book_id))
                assert '675cc7a4-4197-49e5-abf9-1216325fefda' in [str(book_category.category_id) for book_category in
                                                                  book_categories]

        # Author filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'author_ids': ['2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_authors = self.get_async_result(crud.BookAuthorCRUD.get_all(book_id=book_id))
                assert '2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9' in [str(book_author.author_id) for book_author in
                                                                  book_authors]

        # Series filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'series_ids': ['5a539a6f-5415-4cc6-8473-3f17d28cc071']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_series = self.get_async_result(crud.BookSeriesCRUD.get_all(book_id=book_id))
                assert '5a539a6f-5415-4cc6-8473-3f17d28cc071' in [str(book_seria.series_id) for book_seria in
                                                                  book_series]

        # Tag filter
        response = client.get(
            self.get_admin_url('/analytics/read/'),
            headers=self.get_authorization_header(access_token),
            params={'tag_ids': ['096af069-a0e8-4ede-8edc-2a029691abef']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        book_ids = [book.get('id') for book in response_data.get('results')]
        if book_ids:
            for book_id in book_ids:
                book_tags = self.get_async_result(crud.BookTagCRUD.get_all(book_id=book_id))
                assert '096af069-a0e8-4ede-8edc-2a029691abef' in [str(book_tag.tag_id) for book_tag in book_tags]
