from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email адрес")
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name="Номер телефона"
    )
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        blank=True, upload_to="media/avatars", verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
