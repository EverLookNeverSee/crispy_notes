from django.urls import path, include


app_name = "api-v2"

urlpatterns = [
    # accounts
    path("", include("accounts.api.v2.urls.users")),
    path("profile", include("accounts.api.v2.urls.profiles")),
]
