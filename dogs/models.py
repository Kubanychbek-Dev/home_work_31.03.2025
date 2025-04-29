from django.db import models
from django.conf import settings
from users.models import NULLABLE

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.CharField(max_length=800, verbose_name="Description")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="Dog name")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Dog Breed")
    img = models.ImageField(upload_to="dogs/", **NULLABLE, verbose_name="Image")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Owner")

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "Dog"
        verbose_name_plural = "Dogs"


class DogParent(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Parent's name")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Parent's breed")
    birth_date = models.DateField(**NULLABLE, verbose_name="Parent's birthdate")

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"