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
