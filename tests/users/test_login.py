import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_login(api_client, user_factory):
    user = user_factory.create()
    data = {"email": user.email, "password": "password"}

    response = api_client.post(reverse("token_obtain_pair"), data=data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
