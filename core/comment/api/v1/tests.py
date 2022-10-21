import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.views import get_user_model
from django.utils import timezone
from ...models import Comment
from blog.models import Post, Category
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


@pytest.fixture()
@pytest.mark.django_db
def sample_comment(active_user, sample_post, sample_category):
    profile = Profile.objects.get(user__id=active_user.id)
    sample_comment = Comment.objects.create(
        post=sample_post,
        name=f"{profile.first_name} {profile.last_name}",
        email=active_user.email,
        message="This is the comment message.",
    )
    sample_comment.save()
    return sample_comment


@pytest.mark.django_db
class TestCommentApiView:
    def test_get_user_comments_list_successful_status(
        self, api_client, active_user, sample_comment
    ):
        url = reverse("comment:api-v1:comments")
        api_client.force_login(active_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_comment_for_post_successful_status(
        self, api_client, active_user, sample_post
    ):
        url = reverse("comment:api-v1:comments")
        profile = Profile.objects.get(user__id=active_user.id)
        api_client.force_login(active_user)
        data = {
            "post": sample_post.pk,
            "name": f"{profile.first_name} {profile.last_name}",
            "email": active_user.email,
            "message": "This message is for testing comment creation api.",
            "is_approved": True,
        }
        api_client.force_login(active_user)
        response = api_client.post(url, data)
        assert response.status_code == 201
