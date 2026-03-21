from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import AppUser
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(CreateView):

    model = AppUser
    form_class = RegisterForm
    template_name = "accounts/register-page.html"

    success_url = reverse_lazy("login")

class UserLoginView(LoginView):
    template_name = "accounts/login-page.html"

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")



