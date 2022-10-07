from django.urls import path
from .views import CustomLoginView, CustomLogoutView, CustomSignupView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("signup/", CustomSignupView.as_view(), name="signup"),
    # path("activate/<uidb64>/<token>/")
]
