from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from . models import Breed, Dog, DogParent
from .forms import DogForm, DogParentForm


def index_view(request):
    context = {
        "object_list": Breed.objects.all()[:3],
        "title": "PetPlace"
    }
    return render(request, 'dogs/index.html', context=context)


# def breeds_list_view(request):
#     context = {
#         "object_list": Breed.objects.all(),
#         "title": "PetPlace - Все наши породы собак"
#     }
#     return render(request, 'dogs/breeds.html', context=context)


class BreedListView(ListView):
    model = Breed
    extra_context = {
        "title": "All our breeds"
    }
    template_name = "dogs/breeds.html"


def breed_dogs_list_view(request, pk: int):
    breed_obj = Breed.objects.get(pk=pk)
    context = {
        "object_list": Dog.objects.filter(breed_id=pk),
        "title": f"Собаки - {breed_obj.name}",
        "breed_pk": breed_obj.pk
    }
    return render(request, 'dogs/dogs.html', context=context)


# def dogs_list_view(request):
#     context = {
#         "object_list": Dog.objects.all(),
#         "title": "Все собаки",
#     }
#     return render(request, 'dogs/dogs.html', context=context)


class DogListView(ListView):
    model = Dog
    extra_context = {
        "title": "All our dogs"
    }
    template_name = "dogs/dogs.html"


# @login_required(login_url="users:user_login")
# def dog_create_view(request):
#     if request.method == "POST":
#         form = DogForm(request.POST, request.FILES)
#         if form.is_valid():
#             # form.save()
#             dog_object = form.save()
#             dog_object.owner = request.user
#             dog_object.save()
#             return HttpResponseRedirect(reverse("dogs:dogs_list"))
#
#     context = {
#         "title": "Добавить собаку",
#         "form": DogForm
#     }
#     return render(request, "dogs/create.html", context=context)


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/create.html"
    extra_context = {
        "title": "Add dog"
    }
    success_url = reverse_lazy("dogs:dogs_list")
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


# @login_required(login_url="users:user_login")
# def dog_detail_view(request, pk):
#     dog_object = Dog.objects.get(pk=pk)
#     context = {
#         "object": dog_object,
#         "title": dog_object
#     }
#     return render(request, "dogs/detail.html", context=context)


class DogDetailView(DetailView):
    model = Dog
    template_name = "dogs/detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data["title"] = f"All information {object_}"
        return context_data

# @login_required(login_url="users:user_login")
# def dog_update_view(request, pk):
#     dog_object = get_object_or_404(Dog, pk=pk)
#     if request.method == "POST":
#         form = DogForm(request.POST, request.FILES, instance=dog_object)
#         if form.is_valid():
#             dog_object = form.save()
#             dog_object.save()
#             return HttpResponseRedirect(reverse("dogs:dog_detail", args={pk: pk}))
#     context = {
#         "object": dog_object,
#         "title": "Изменить данные",
#         "form": DogForm(instance=dog_object)
#     }
#     return render(request, "dogs/create.html", context=context)


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(Dog, DogParent, form=DogParentForm, extra=1)
        if self.request.method == "POST":
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        object_ = self.get_object()
        context_data["title"] = f"Change information of {object_}"
        context_data["formset"] = formset
        return context_data
    
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dogs:dog_detail", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


# @login_required(login_url="users:user_login")
# def dog_delete_view(request, pk):
#     dog_object = get_object_or_404(Dog, pk=pk)
#     if request.method == "POST":
#         dog_object.delete()
#         return HttpResponseRedirect(reverse("dogs:dogs_list"))
#     context = {
#         "object": dog_object,
#         "title": "Удалить данные",
#     }
#     return render(request, "dogs/delete.html", context=context)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = "dogs/delete.html"
    success_url = reverse_lazy("dogs:dogs_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data["title"] = f"Delete the {object_}"
        return context_data
