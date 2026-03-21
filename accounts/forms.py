from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = AppUser
        fields = ("email",)