from django.urls import path, include
from .views import CommentCreateView

app_name = "comment"

urlpatterns = [
    path("<int:pk>/add/", CommentCreateView.as_view(), name="create"),
    path("api/v1/", include("comment.api.v1.urls")),
]
