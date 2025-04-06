from django.shortcuts import render
from . models import Breed, Dog


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