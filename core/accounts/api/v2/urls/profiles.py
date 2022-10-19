from django.urls import path
from .. import views


urlpatterns = [
    # --- profiles ---
    path("", views.ProfileAPIView.as_view(), name="profile")
]
