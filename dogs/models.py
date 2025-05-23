from django.db import models
from django.conf import settings
from users.models import NULLABLE


class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.CharField(max_length=800, verbose_name="Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя собаки")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Порода собаки")
    img = models.ImageField(upload_to="dogs/", **NULLABLE, verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "Dog"
        verbose_name_plural = "Dogs"

    def views_count(self):
        self.views += 1
        self.save()


class DogParent(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Имя родителя")
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name="Родительская порода")
    birth_date = models.DateField(**NULLABLE, verbose_name="Дата рождения родителя")

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"
