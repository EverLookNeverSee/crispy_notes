import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.views import get_user_model
from django.utils import timezone
from ...models import Comment
from blog.models import Post, Category
from accounts.models import Profile

User = get_user_model()
