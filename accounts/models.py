from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import AppUserManager   # 🔥 важно


class AppUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ("manager", "Мениджър"),
        ("user", "Потребител"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AppUserManager()   # 🔥 НАЙ-ВАЖНОТО

    def __str__(self):
        return self.email