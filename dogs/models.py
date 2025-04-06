from django.db import models
from users.models import NULLABLE

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    description = models.CharField(max_length=800, verbose_name="description")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "breed"
        verbose_name_plural = "breeds"


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="dog name")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="breed")
    img = models.ImageField(upload_to="dogs/", **NULLABLE, verbose_name="image")

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "dog"
        verbose_name_plural = "dogs"
