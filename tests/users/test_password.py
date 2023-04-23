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
