import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.views import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
