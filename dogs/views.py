from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from . models import Breed, Dog
from .forms import DogForm


def index_view(request):
    context = {
        "object_list": Breed.objects.all()[:3],
        "title": "PetShop - Главное"
    }
    return render(request, 'dogs/index.html', context=context)


def breeds_list_view(request):
    context = {
        "object_list": Breed.objects.all(),
        "title": "PetShop - Все наши породы собак"
    }
    return render(request, 'dogs/breeds.html', context=context)


def breed_dogs_list_view(request, pk: int):
    breed_obj = Breed.objects.get(pk=pk)
    context = {
        "object_list": Dog.objects.filter(breed_id=pk),
        "title": f"Собаки - {breed_obj.name}",
        "breed_pk": breed_obj.pk
    }
    return render(request, 'dogs/dogs.html', context=context)


def dogs_list_view(request):
    context = {
        "object_list": Dog.objects.all(),
        "title": "Все собаки",
    }
    return render(request, 'dogs/dogs.html', context=context)


def dog_create_view(request):
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dogs:dogs_list"))

    context = {
        "title": "Добавить собаку",
        "form": DogForm
    }
    return render(request, "dogs/create.html", context=context)


def dog_detail_view(request, pk):
    dog_object = Dog.objects.get(pk=pk)
    context = {
        "object": dog_object,
        "title": dog_object
    }
    return render(request, "dogs/detail.html", context=context)


def dog_update_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse("dogs:dog_detail", args={pk: pk}))
    context = {
        "object": dog_object,
        "title": "Изменить данные",
        "form": DogForm(instance=dog_object)
    }
    return render(request, "dogs/update.html", context=context)


def dog_delete_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        dog_object.deleete()
        return HttpResponseRedirect(reverse("dogs:dogs_list"))
    context = {
        "object": dog_object,
        "title": "Удалить данные",
    }
    return render(request, "dogs/delete.html", context=context)
