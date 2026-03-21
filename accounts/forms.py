from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AppUser


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "placeholder": "example@email.com"
        })
    )

    first_name = forms.CharField(
        label="Собствено име",
        widget=forms.TextInput(attrs={
            "placeholder": "Въведете име"
        })
    )

    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            "placeholder": "Въведете фамилия"
        })
    )

    password1 = forms.CharField(
        label="Парола",
        help_text="""
            • Минимум 8 символа<br>
            • Да не съдържа лична информация<br>
            • Да не е често използвана парола<br>
            • Да не е само цифри
            """,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Въведете парола"
        })
    )

    password2 = forms.CharField(
        label="Потвърди парола",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Повторете паролата"
        })
    )

    class Meta:
        model = AppUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

class LoginForm(AuthenticationForm):

    username = forms.CharField(label="E-mail")

    password = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Въведете парола"
        })
    )