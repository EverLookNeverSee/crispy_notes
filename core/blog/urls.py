from django.urls import path
from .views import (
    BlogIndexView,
    PostDetailView,
    CategoryFilterPostListView,
    AuthorFilterPostListView,
    SearchPostListView,
)


app_name = "blog"

urlpatterns = [
    path("", BlogIndexView.as_view(), name="index"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("category/<str:cat_name>/", CategoryFilterPostListView.as_view(), name="category"),
    path("author/<str:author_email>/", AuthorFilterPostListView.as_view(), name="author"),
    path("search/", SearchPostListView.as_view(), name="search"),
]
