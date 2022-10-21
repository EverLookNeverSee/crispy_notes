import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.views import get_user_model
from django.utils import timezone
from ...models import Category, Post
from accounts.models import Profile

User = get_user_model()


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
@pytest.mark.django_db
def active_user():
    user = User.objects.create_user(
        email="active_user@test.com", password="A@123456", is_verified=True
    )
    user.save()
    return user


@pytest.fixture()
@pytest.mark.django_db
def sample_categories():
    categories_list = ["Test1", "Test2", "Test3", "Test4", "Test5"]
    for item in categories_list:
        cat = Category.objects.create(name=item)
        cat.save()
    cats = Category.objects.all()
    return cats


@pytest.fixture()
@pytest.mark.django_db
def sample_category():
    sample_cat = Category.objects.create(name="Sample_Cat")
    return sample_cat


@pytest.fixture()
@pytest.mark.django_db
def sample_post(active_user, sample_category):
    sample_post = Post.objects.create(
        author=Profile.objects.get(user__id=active_user.id),
        title="Test post",
        content="This is the test post content.",
        ok_to_publish=True,
        publish_date=timezone.now(),
    )
    sample_post.category.set([sample_category])
    sample_post.save()
    return sample_post


@pytest.mark.django_db
class TestCategoryApiViewSet:
    def test_get_list_of_categories_successful_status(
        self, api_client, active_user, sample_categories
    ):
        url = reverse("blog:api-v1:category-list")
        api_client.force_login(active_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_category_detail_successful_status(
        self, api_client, active_user, sample_categories
    ):
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": 1})
        api_client.force_login(active_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_category_successful_status(self, api_client, active_user):
        url = reverse("blog:api-v1:category-list")
        data = {"name": "Fun"}
        api_client.force_login(active_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_get_category_by_id_successful_status(
        self, api_client, active_user, sample_categories
    ):
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": 1})
        api_client.force_login(active_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_patch_category_by_id_successful_status(
        self, api_client, active_user, sample_categories
    ):
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": 1})
        data = {"name": "Aero"}
        api_client.force_login(active_user)
        response = api_client.patch(url, data)
        assert response.status_code == 200

    def test_delete_category_by_id_successful_status(
        self, api_client, active_user, sample_categories
    ):
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": 1})
        api_client.force_login(active_user)
        response = api_client.delete(url)
        assert response.status_code == 204
