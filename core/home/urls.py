from django.urls import path
from django.views.decorators.cache import cache_page
from .views import IndexPageView, AboutPageView, ContactPageView

app_name = "home"

urlpatterns = [
    path("", cache_page(timeout=60 * 60)(IndexPageView.as_view()), name="index"),
    path("about/", cache_page(timeout=60 * 60)(AboutPageView.as_view()), name="about"),
    path(
        "contact/",
        cache_page(timeout=60 * 60)(ContactPageView.as_view()),
        name="contact",
    ),
]
