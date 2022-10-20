from django.urls import path
from .views import CommentApiView

app_name = "api-v1"

urlpatterns = [
    path("comments/", CommentApiView.as_view(), name="comments"),
]
