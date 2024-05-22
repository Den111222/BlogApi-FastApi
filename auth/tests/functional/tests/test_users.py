import jwt
from random import choice

import pytest
from httpx import AsyncClient
from fastapi import status

from core.config import app_settings_test
from tests.functional.testdata.users_data import (
    users_data,
    not_exist_users_data,
    invalid_users_data,
)


@pytest.mark.asyncio
class TestUser:
    exist_user_data = choice(users_data)
    not_exist_user_data = choice(not_exist_users_data)
    invalid_users_data = choice(invalid_users_data)

    @staticmethod
    def _prepare_data(_data: dict, fields: list):
        return {fld: _data[fld] for fld in fields}

    @pytest.mark.parametrize(
        "user_data, expected_answer",
        [
            (exist_user_data, {"status": status.HTTP_200_OK}),
            (not_exist_user_data, {"status": status.HTTP_404_NOT_FOUND}),  # not exist
        ],
    )
    async def test_get_user(
        self, ac: AsyncClient, user_data: dict, expected_answer: dict
    ):
        response = await ac.get(f"/api/v1/users/{user_data['id']}")
        assert response.status_code == expected_answer["status"]
        if response.status_code == status.HTTP_200_OK:
            body = response.json()
            assert body.get("login") == user_data["login"]
            assert body.get("email") == user_data["email"]
            assert body.get("id") == user_data["id"]

    @pytest.mark.parametrize(
        "user_data, expected_answer",
        [
            (
                {
                    "login": "new_user",
                    "email": "new_user@mail.com",
                    "password": "new_user",
                },  # not exist
                {"status": status.HTTP_201_CREATED},
            ),
            (
                {
                    "login": "new_user",
                    "email": "new_user@mail.com",
                    "password": "new_user",
                },  # already exists
                {"status": status.HTTP_400_BAD_REQUEST},
            ),
            (
                _prepare_data(not_exist_user_data, ["login", "email"]),  # invalid data
                {"status": status.HTTP_422_UNPROCESSABLE_ENTITY},
            ),
            (
                _prepare_data(
                    invalid_users_data, ["login", "email", "password"]
                ),  # invalid data
                {"status": status.HTTP_422_UNPROCESSABLE_ENTITY},
            ),
        ],
    )
    async def test_signup(
        self, ac: AsyncClient, user_data: dict, expected_answer: dict
    ):
        response = await ac.post("/api/v1/users/signup", json=user_data)
        assert response.status_code == expected_answer["status"]
        if response.status_code == status.HTTP_201_CREATED:
            body = response.json()
            assert body.get("login") == user_data["login"]
            assert body.get("email") == user_data["email"]

    @pytest.mark.parametrize(
        "user_data, expected_answer",
        [
            (
                _prepare_data(exist_user_data, ["login", "password"]),
                {"status": status.HTTP_200_OK},
            ),
            (
                _prepare_data(not_exist_user_data, ["login", "password"]),
                {"status": status.HTTP_401_UNAUTHORIZED},
            ),
            (
                _prepare_data(not_exist_user_data, ["login"]),
                {"status": status.HTTP_422_UNPROCESSABLE_ENTITY},
            ),
        ],
    )
    async def test_login(self, ac: AsyncClient, user_data: dict, expected_answer: dict):
        response = await ac.post("/api/v1/users/login", json=user_data)
        assert response.status_code == expected_answer["status"]
        if response.status_code == status.HTTP_200_OK:
            body = response.json()
            assert body.get("access_token") is not None
            assert body.get("refresh_token") is not None
            payload = jwt.decode(
                body.get("access_token"),
                app_settings_test.token_secret,
                algorithms=[app_settings_test.algorithm],
            )
            assert user_data["login"] == payload["login"]

            # refresh token check
            response2 = await ac.post(
                "/api/v1/users/refresh",
                cookies={"refresh_token": body.get("refresh_token")},
            )
            body2 = response2.json()
            assert body2.get("access_token") is not None
            assert body2.get("refresh_token") is not None
            assert body.get("access_token") != body2.get("access_token")
            assert body.get("refresh_token") != body2.get("refresh_token")
            payload2 = jwt.decode(
                body2.get("access_token"),
                app_settings_test.token_secret,
                algorithms=[app_settings_test.algorithm],
            )
            assert user_data["login"] == payload2["login"]

    @pytest.mark.parametrize(
        "user_data, expected_answer",
        [
            (
                _prepare_data(exist_user_data, ["login", "password", "id"]),
                {"status": status.HTTP_200_OK},
            ),
            (
                {"id": "123"},  # invalid data
                {"status": status.HTTP_422_UNPROCESSABLE_ENTITY},
            ),
            (
                {"id": ""},  # invalid data
                {"status": status.HTTP_307_TEMPORARY_REDIRECT},
            ),
        ],
    )
    async def test_history(
        self, ac: AsyncClient, user_data: dict, expected_answer: dict
    ):
        response = await ac.get(f"/api/v1/users/history/{user_data['id']}")
        assert response.status_code == expected_answer["status"]
        if response.status_code == status.HTTP_200_OK:
            body = response.json()
            count = len(body)

            login_data = self._prepare_data(user_data, ["login", "password"])
            resp_login = await ac.post("/api/v1/users/login", json=login_data)
            assert resp_login.status_code == status.HTTP_200_OK

            response2 = await ac.get(f"/api/v1/users/history/{user_data['id']}")
            assert response2.status_code == expected_answer["status"]
            if response2.status_code == status.HTTP_200_OK:
                body2 = response2.json()
                count2 = len(body2)
                assert count2 == count + 1
