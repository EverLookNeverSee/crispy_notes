from django.urls import path
from .views import IndexPageView, AboutPageView, ContactPageView

app_name = "home"

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
]
