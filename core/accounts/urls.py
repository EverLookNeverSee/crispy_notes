from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomSignupView,
    UserVerificationView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("signup/", CustomSignupView.as_view(), name="signup"),
    path(
        "verification/<uidb64>/<token>/",
        UserVerificationView.as_view(),
        name="verification",
    ),
]
