import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.views import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
@pytest.mark.django_db
def common_user():
    user = User.objects.create_user(
        email="test_user@test.com",
        password="A@123456",
    )
    user.save()
    return user


@pytest.fixture()
@pytest.mark.django_db
def active_user():
    user = User.objects.create_user(
        email="active_user@test.com",
        password="A@123456",
        is_verified=True
    )
    user.save()
    return user


@pytest.mark.django_db
class TestRegistrationAPIView:
    def test_register_user_successfully_status(self, api_client):
        url = reverse("accounts:api-v2:registration")
        data = {
            "email": "test_user@test.com",
            "password": "A@123456",
            "password1": "A@123456"
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_common_user_fields(self, common_user):
        assert common_user.email == "test_user@test.com"
        assert common_user.is_verified is False
        assert common_user.id == 1

    def test_active_user_fields(self, active_user):
        assert active_user.email == "active_user@test.com"
        assert active_user.is_verified is True
        assert active_user.id == 1


@pytest.mark.django_db
class TestActivationAPIView:
    def test_user_activation_successfully_status(self, common_user, api_client):
        user_token = str(RefreshToken.for_user(common_user).access_token)
        url = reverse("accounts:api-v2:activation", kwargs={"token": user_token})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_user_activation_invalid_token_status(self, common_user, api_client):
        user_token = str(RefreshToken.for_user(common_user).access_token)
        url = reverse("accounts:api-v2:activation", kwargs={"token": f"{user_token}1"})
        response = api_client.get(url)
        assert response.status_code == 400

