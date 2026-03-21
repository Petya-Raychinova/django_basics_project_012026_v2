from django.urls import path
from .views import RegisterView, UserLoginView, UserLogoutView, profile_view

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
]