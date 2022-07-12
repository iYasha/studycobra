import json
from typing import List, Dict

from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAdminWidgets(TestBase):
    """Тесты для проверки работоспособности АПИ виджетов"""

    widget_id = 'abbfa2d0-fc02-4d90-9e44-9d5e1e5edc28'

    def test_create_widget(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/widgets/'),
            json={
                "language": "ru",
                "widget_type": "carousel",
                "cover_type": "image",
                "title": "string",
                "collection_id": None,
                'background_for_ipad': None,
                "background_color": "string",
                "text_color": "string",
                "index": 3,
                "file_id": "e92ff362-41f7-409c-99fc-62b8570ffcde",
                "is_active": True,
                "book_id": None
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'language', 'widget_type', 'cover_type', 'title', 'collection_id',
            'background_color', 'text_color', 'index', 'file_id', 'is_active', 'book_id', 'id', 'file',
            'background_for_ipad'))

    def test_get_widgets_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/widgets/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Widget 1'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(widget.get('language') for widget in response_data.get('results')) == {'ru'}
        assert response_data.get('results')[0].get('title') == 'Widget 1'

    def test_get_widgets(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/widgets/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(widget.get('language') for widget in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), (
            'created_at', 'updated_at', 'language', 'widget_type', 'cover_type', 'title', 'collection_id',
            'background_color', 'text_color', 'index', 'file_id', 'is_active', 'book_id', 'id', 'file', 'age_groups',
            'background_for_ipad'))

    def test_get_one_widget(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/widgets/{self.widget_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK

        self.assert_keys(tuple(response_data.keys()), (
            'created_at', 'updated_at', 'language', 'widget_type', 'cover_type', 'title', 'collection_id',
            'background_color', 'text_color', 'index', 'file_id', 'is_active', 'book_id', 'id', 'file',
            'background_for_ipad'))

    def test_update_widget(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/widgets/{self.widget_id}'),
            json={
                "language": "ru",
                "widget_type": "collection_pages",
                "cover_type": "image",
                "title": "updated_widget",
                "collection_id": "9af897fb-ce5d-432b-86d9-4340c0f6ea04",
                "background_color": "black",
                'background_for_ipad': None,
                "text_color": "red",
                "index": 4,
                "file_id": "1257e579-7ca1-476f-aee9-4d58f74ca575",
                "is_active": False,
                "book_id": "f4afa085-601c-4157-9c89-9ae069eeffed"
            },
            headers=self.get_authorization_header(access_token),
        )
        widget = self.get_async_result(crud.WidgetAdminCRUD.get_one(id=self.widget_id))

        data = json.loads(widget.json())
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert data == {
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
            "language": "ru",
            "widget_type": "collection_pages",
            "cover_type": "image",
            "title": "updated_widget",
            "collection_id": "9af897fb-ce5d-432b-86d9-4340c0f6ea04",
            "background_color": "black",
            'background_for_ipad': None,
            "text_color": "red",
            "index": data.get('index'),
            "file_id": "1257e579-7ca1-476f-aee9-4d58f74ca575",
            "is_active": False,
            "book_id": "f4afa085-601c-4157-9c89-9ae069eeffed",
            "id": data.get('id'),
            "file": data.get('file'),
        }

    def test_delete_widget(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/widgets/{self.widget_id}'),
            headers=self.get_authorization_header(access_token),
        )
        widget = self.get_async_result(crud.WidgetAdminCRUD.get_one(id=self.widget_id))
        assert widget is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='ru'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

    def test_duplicate_widget(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/widgets/{self.widget_id}/duplicate/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK
        except_fields = {'created_at', 'file', 'index', 'id'}
        response_data = {key: value for key, value in response.json().items() if key not in except_fields}
        old_widget = json.loads(self.get_async_result(crud.WidgetAdminCRUD.get_one(id=self.widget_id)).json(
            exclude=except_fields))
        assert response_data == old_widget
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='ru'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

    def test_create_widget_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "widget_type": "carousel",
            "cover_type": "image",
            "title": "string",
            "collection_id": None,
            "background_color": "string",
            'background_for_ipad': None,
            "text_color": "string",
            "index": 100,
            "file_id": "e92ff362-41f7-409c-99fc-62b8570ffcde",
            "is_active": True,
            "book_id": None
        }
        response_big_index = client.post(
            self.get_admin_url('/widgets/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_200_OK
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='ru'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

        request['index'] = 2
        response_small_index = client.post(
            self.get_admin_url('/widgets/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_200_OK
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='ru'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

    def test_update_widget_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "widget_type": "collection_pages",
            "cover_type": "image",
            "title": "updated_widget",
            "collection_id": "9af897fb-ce5d-432b-86d9-4340c0f6ea04",
            "background_color": "black",
            "background_for_ipad": None,
            "text_color": "red",
            "index": 100,
            "file_id": "1257e579-7ca1-476f-aee9-4d58f74ca575",
            "is_active": False,
            "book_id": "f4afa085-601c-4157-9c89-9ae069eeffed"
        }
        response_big_index = client.put(
            self.get_admin_url(f'/widgets/{self.widget_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_204_NO_CONTENT
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='en'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))
        request['index'] = 2
        response_small_index = client.put(
            self.get_admin_url(f'/widgets/{self.widget_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_204_NO_CONTENT
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='en'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

    def test_swap_index_in_widgets(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        first_widget_before = self.get_async_result(
            crud.WidgetAdminCRUD.get_one(id='abbfa2d0-fc02-4d90-9e44-9d5e1e5edc28'))
        second_widget_before = self.get_async_result(
            crud.WidgetAdminCRUD.get_one(id='7325350b-2afa-443d-a596-d5d12aef7e8d'))

        response = client.put(
            self.get_admin_url(f'/widgets/swap/'),
            json={
                "first_obj_pk": 'abbfa2d0-fc02-4d90-9e44-9d5e1e5edc28',
                "second_obj_pk": '7325350b-2afa-443d-a596-d5d12aef7e8d'
            },
            headers=self.get_authorization_header(access_token),
        )
        first_widget_after = self.get_async_result(
            crud.WidgetAdminCRUD.get_one(id='abbfa2d0-fc02-4d90-9e44-9d5e1e5edc28'))
        second_widget_after = self.get_async_result(
            crud.WidgetAdminCRUD.get_one(id='7325350b-2afa-443d-a596-d5d12aef7e8d'))
        assert first_widget_before.index == second_widget_after.index
        assert first_widget_after.index == second_widget_before.index
        assert response.status_code == status.HTTP_204_NO_CONTENT
        widgets = self.get_async_result(crud.WidgetAdminCRUD.get_all(language='ru'))
        self.assert_keys([widget.index for widget in widgets], list(range(1, len(widgets) + 1)))

    def test_get_widget_preview(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/widgets/{self.widget_id}/preview/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'title', 'background_color', 'text_color', 'book', 'books', 'file_id', 'widget_image'))

    def test_get_widget_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        widget_types = ('carousel', 'collection_pages', 'collection_readme', 'one_book_pages', 'one_book_readme',
                        'one_book_audio', 'video')
        for widget_type in widget_types:
            response = client.get(
                self.get_admin_url(f'/widgets/settings/'),
                headers=self.get_authorization_header(access_token),
                params={'widget_type': widget_type}
            )
            response_data = response.json()
            assert response.status_code == status.HTTP_200_OK
            self.assert_keys(response_data.keys(), (
                'background_color', 'text_color', 'cover_type', 'background_for_ipad', 'file_id', 'widget_image'
            ))

    def test_post_widget_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        widget_types = ('carousel', 'collection_pages', 'collection_readme', 'one_book_pages', 'one_book_readme',
                        'one_book_audio', 'video')

        def set_widget_settings(request: Dict[str, str], widget_type: str, assert_fields: List[str]):
            response = client.post(
                self.get_admin_url(f'/widgets/settings/'),
                headers=self.get_authorization_header(access_token),
                params={'widget_type': widget_type},
                json=request
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT
            carousel_settings = self.get_async_result(crud.WidgetAdminCRUD.get_settings(
                widget_type=widget_type,
                language='ru')
            )
            for field in assert_fields:
                assert str(getattr(carousel_settings, field)) == request.get(field)

        set_widget_settings(
            request={
                "background_color": "white",
                "text_color": "orange",
            },
            widget_type=widget_types[0],
            assert_fields=['background_color', 'text_color'])

        set_widget_settings(
            request={
                "background_for_ipad": "white",
                "text_color": "orange",
            },
            widget_type=widget_types[1],
            assert_fields=['background_for_ipad', 'text_color'])

        set_widget_settings(
            request={
                "background_for_ipad": "white",
                "text_color": "orange",
            },
            widget_type=widget_types[2],
            assert_fields=['background_for_ipad', 'text_color'])

        set_widget_settings(
            request={
                "background_color": "white",
                "background_for_ipad": "white",
                "text_color": "orange",
                "file_id": "a99341a0-c00d-4ba9-83dc-6673b460d9fb"
            },
            widget_type=widget_types[3],
            assert_fields=['background_color', 'background_for_ipad', 'text_color', 'file_id'])

        set_widget_settings(
            request={
                "background_color": "white",
                "background_for_ipad": "white",
                "file_id": "0049f69a-ae8a-4eb6-8b8b-996f9071f9bc"
            },
            widget_type=widget_types[4],
            assert_fields=['background_color', 'background_for_ipad', 'file_id'])
