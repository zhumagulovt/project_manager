import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.fixture
def user_data():
    data = {
        "first_name": "Name",
        "last_name": "Lastname",
        "email": "username@email.com",
        "password": "Testpassword",
        "password_confirm": "Testpassword",
    }
    return data


@pytest.mark.django_db
class TestRegistration:
    def test_registration(self, api_client, user_data):
        response = api_client.post(
            "/api/v1/users/registration/", data=user_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1

    def test_registration_with_existing_username(
        self, api_client, user_factory, user_data
    ):
        user_factory.create()

        # copy email of existing user
        user_data["email"] = user_factory.email
        response = api_client.post(
            "/api/v1/users/registration/", data=user_data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_with_incorrect_password_confirmation(
        self, api_client, user_data
    ):
        user_data["password_confirm"] = user_data["password"][1:]

        response = api_client.post(
            "/api/v1/users/registration/", data=user_data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        "password, status_code",
        [
            ("qwerty123", 400),
            ("12345678", 400),
            ("password", 400),
            ("R11$1q_", 400),
        ],
    )
    def test_registration_with_invalid_password(
        self, password, status_code, api_client, user_data
    ):
        user_data["password"] = password
        user_data["password_confirm"] = password

        response = api_client.post(
            "/api/v1/users/registration/", data=user_data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
