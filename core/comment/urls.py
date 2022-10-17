from django.urls import path
from .views import CommentCreateView

app_name = "comment"

urlpatterns = [
    path("/<int:pk>/add/", CommentCreateView.as_view(), name="create"),
]
