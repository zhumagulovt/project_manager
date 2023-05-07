from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPassword:
    @pytest.mark.parametrize(
        "current_password, new_password, status_code",
        [
            ("password", "Password_", 200),
            ("invalid_password", "Password_", 400),
            ("password", "password", 400),
            ("password", "qwertyui", 400),
            ("password", "abcdefgh", 400),
        ],
    )
    def test_change_password(
        self, current_password, new_password, status_code, logged_in_client
    ):
        api_client, user = logged_in_client

        data = {
            "current_password": current_password,
            "new_password": new_password,
        }
        response = api_client.post(reverse("change_password"), data=data)

        assert response.status_code == status_code

        if response.status_code == status.HTTP_200_OK:
            user.refresh_from_db()
            assert user.check_password(new_password) is True

    @patch("project_manager.users.tasks.send_reset_password_link_task.delay")
    def test_reset_password(
        self, mock_reset_password, api_client, user_factory
    ):
        user = user_factory()

        response = api_client.post(
            reverse("reset_password"), data={"email": user.email}
        )

        assert response.status_code == status.HTTP_200_OK

        # parse link in email message to get uid and token
        args, kwargs = mock_reset_password.call_args
        query_params = parse_qs(urlparse(kwargs["reset_password_link"]).query)

        data = {
            "uid": query_params["uid"][0],
            "token": query_params["token"][0],
            "password": "NewPAssword_",
            "password_confirm": "NewPAssword_",
        }

        response = api_client.post(
            reverse("reset_password_complete"), data=data
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(data["password"]) is True
