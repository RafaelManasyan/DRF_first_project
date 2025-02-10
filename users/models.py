from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email адрес")
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name="Номер телефона"
    )
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        blank=True, upload_to="media/avatars", verbose_name="Аватар"
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey('web_sky.Course', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey('web_sky.Lesson', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(choices=METHOD_CHOICES, max_length=10, verbose_name='Способ оплаты')
