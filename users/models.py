from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {"blank": True, "null": True}


class UserRoles(models.TextChoices):
    ADMIN = "admin", _("admin")
    MODERATOR = "moderator", _("moderator")
    USER = "user", _("user")


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    role = models.CharField(max_length=18, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=100, verbose_name="Имя", default="Not specified")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", default="Not specified")
    phone = models.CharField(max_length=35, unique=True, verbose_name="Телефон", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Activity")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "User"
        ordering = ["id"]