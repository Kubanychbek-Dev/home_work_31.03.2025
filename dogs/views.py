from django.shortcuts import render
from . models import Breed


def index_view(request):
    context = {
        "object_list": Breed.objects.all(),
        "title": "PetShop - Главное"
    }
    return render(request, 'dogs/index.html', context=context)