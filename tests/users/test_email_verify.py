from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture
@patch("project_manager.users.tasks.send_email_confirmation_link_task.delay")
def new_user(mock_email_confirmation, api_client):
    data = {
        "first_name": "Name",
        "last_name": "Lastname",
        "email": "raletab769@ippals.com",
        "password": "Testpassword",
        "password_confirm": "Testpassword",
    }

    reverse("registration")
    api_client.post(reverse("registration"), data=data)

    args, kwargs = mock_email_confirmation.call_args

    return User.objects.get(email=data["email"]), kwargs["verification_link"]


@pytest.mark.django_db
class TestEmailVerify:
    def test_verify_email(self, api_client, new_user, settings):
        user, verification_link = new_user

        assert user.is_active is False

        response = api_client.get(verification_link)

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.is_active is True

    @pytest.mark.parametrize(
        "index",
        [4, 5],
    )
    def test_verify_email_with_invalid_data(self, index, api_client, new_user):
        user, verification_link = new_user

        parts = urlparse(verification_link).path.strip("/").split("/")
        # change uid or token
        parts[index] = parts[index][1:]

        verification_link = "/" + "/".join(parts) + "/"

        response = api_client.get(verification_link)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        user.refresh_from_db()
        assert user.is_active is False
