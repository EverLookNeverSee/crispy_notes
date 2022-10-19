from django.urls import path
from .. import views
from ..views import CustomAuthToken, CustomDiscardAuthToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    # --- accounts ---
    # Registration
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration",
    ),
    # Activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationAPIView.as_view(),
        name="activation",
    ),
    # Resend activation
    path(
        "activation/resend/",
        views.ActivationResendAPIView.as_view(),
        name="activation_resend",
    ),
    # Test email
    # path("test-email/", views.TestEmailSend.as_view(), name="test-email"),
    # Password change
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    # Token
    path("token/login/", CustomAuthToken.as_view(), name="token_login"),
    path("token/logout/", CustomDiscardAuthToken.as_view(), name="token_logout"),
    # JWT
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt_create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
]
