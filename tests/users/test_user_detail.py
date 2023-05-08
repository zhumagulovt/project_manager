import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserDetail:
    def test_change_name(self, logged_in_client, user_factory):
        api_client, user = logged_in_client

        updated_user_data = user_factory.build()

        data = {
            "first_name": updated_user_data.first_name,
            "last_name": updated_user_data.last_name,
            "email": updated_user_data.email,
        }

        assert user.first_name != updated_user_data.first_name
        assert user.last_name != updated_user_data.last_name
        assert user.email != updated_user_data.email

        response = api_client.patch(reverse("user-detail"), data=data)

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.first_name == updated_user_data.first_name
        assert user.last_name == updated_user_data.last_name
        assert user.email == updated_user_data.email
