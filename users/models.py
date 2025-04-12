from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    first_name = models.CharField(max_length=100, verbose_name="First Name", default="Not specified")
    last_name = models.CharField(max_length=100, verbose_name="Last Name", default="Not specified")
    phone = models.CharField(max_length=35, unique=True, verbose_name="phone", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Avatar", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Activity")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "User"
        ordering = ["id"]