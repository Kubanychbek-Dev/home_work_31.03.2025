from django.contrib import admin

from . models import Breed, Dog


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    ordering = ("pk",)


@admin.register(Dog)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "breed",)
    list_filter = ("breed",)
    ordering = ("name",)