from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAdminLocalization(TestBase):
    """Тесты для проверки работоспособности АПИ локализации"""

    locale = 'en'

    def test_get_available_languages(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/localizations/language/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('language', 'locale'))

    def test_already_exists_localization(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/localizations/'),
            json={
                "language": "English",
                "locale": "en",
                "index": 15,
                "is_active": True
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data.get('field_errors')[0].get('message') == 'Pair language-locale already exists'

    def test_create_localization(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/localizations/'),
            json={
                "language": "Arabic",
                "locale": "ar",
                "index": 7,
                "is_active": True
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'language', 'locale', 'index', 'is_active'
        ))

    def test_get_localizations(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/localizations/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), (
            'created_at', 'updated_at', 'language', 'locale', 'index', 'is_active'
        ))

    def test_get_one_localization(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/localizations/{self.locale}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'language', 'locale', 'index', 'is_active'
        ))

    def test_update_localization(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/localizations/{self.locale}'),
            json={
                "index": 1,
                "is_active": False
            },
            headers=self.get_authorization_header(access_token),
        )
        localization = self.get_async_result(crud.LocalizationCRUD.get_one(locale=self.locale))
        assert localization.language == 'English'
        assert localization.locale == 'en'
        assert localization.index == 1
        assert not localization.is_active
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_localization(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/localizations/{self.locale}'),
            headers=self.get_authorization_header(access_token),
        )
        localization = self.get_async_result(crud.LocalizationCRUD.get_one(locale=self.locale))
        books = self.get_async_result(crud.BookCRUD.get_all(language=self.locale))
        age_groups = self.get_async_result(crud.AgeGroupCRUD.get_all(language=self.locale))
        categories = self.get_async_result(crud.CategoryAdminCRUD.get_all(language=self.locale))
        authors = self.get_async_result(crud.AuthorCRUD.get_all(language=self.locale))
        collections = self.get_async_result(crud.CollectionAdminCRUD.get_all(language=self.locale))
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language=self.locale))
        most_popular_requests = self.get_async_result(crud.MostPopularRequestCRUD.get_all(language=self.locale))
        series = self.get_async_result(crud.SeriesCRUD.get_all(language=self.locale))
        tags = self.get_async_result(crud.TagCRUD.get_all(language=self.locale))
        publishers = self.get_async_result(crud.PublisherCRUD.get_all(language=self.locale))

        assert localization is None
        assert books == []
        assert age_groups == []
        assert categories == []
        assert authors == []
        assert collections == []
        assert widgets == []
        assert series == []
        assert most_popular_requests == []
        assert tags == []
        assert publishers == []
        assert response.status_code == status.HTTP_204_NO_CONTENT
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all(language='ru'))
        self.assert_keys([localization.index for localization in localizations], list(range(1, len(localizations) + 1)))

    def test_create_category_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "Afar",
            "locale": "aa",
            "index": 100,
            "is_active": True
        }
        response_big_index = client.post(
            self.get_admin_url('/localizations/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_200_OK
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all(language='ru'))
        self.assert_keys([locatization.index for locatization in localizations], list(range(1, len(localizations) + 1)))

        request['index'] = 2
        request['language'] = 'Abkhazian'
        request['locale'] = 'ab'
        response_small_index = client.post(
            self.get_admin_url('/localizations/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_200_OK
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all(language='ru'))
        self.assert_keys([localization.index for localization in localizations], list(range(1, len(localizations) + 1)))

    def test_update_category_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "index": 1,
            "is_active": False
        }
        response_big_index = client.put(
            self.get_admin_url(f'/localizations/{self.locale}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_204_NO_CONTENT
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all(language='ru'))
        self.assert_keys([localization.index for localization in localizations], list(range(1, len(localizations) + 1)))
        request['index'] = 2
        response_small_index = client.put(
            self.get_admin_url(f'/localizations/{self.locale}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_204_NO_CONTENT
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all(language='ru'))
        self.assert_keys([localization.index for localization in localizations], list(range(1, len(localizations) + 1)))

    def test_swap_index_in_localizations(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        first_localization_before = self.get_async_result(crud.LocalizationCRUD.get_one(index=1))
        second_localization_before = self.get_async_result(crud.LocalizationCRUD.get_one(index=2))

        response = client.put(
            self.get_admin_url(f'/localizations/swap/'),
            json={
                "first_obj_pk": 'ru',
                "second_obj_pk": 'en'
            },
            headers=self.get_authorization_header(access_token),
        )
        first_localization_after = self.get_async_result(crud.LocalizationCRUD.get_one(index=2))
        second_localization_after = self.get_async_result(crud.LocalizationCRUD.get_one(index=1))
        assert first_localization_before.locale == first_localization_after.locale
        assert second_localization_before.locale == second_localization_after.locale
        assert response.status_code == status.HTTP_204_NO_CONTENT
        localizations = self.get_async_result(crud.LocalizationCRUD.get_all())
        self.assert_keys([localization.index for localization in localizations], list(range(1, len(localizations) + 1)))
