from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from . models import Breed, Dog, DogParent
from .forms import DogForm, DogParentForm, DogAdminForm
from .services import send_views_email
from users.models import UserRoles


def index_view(request):
    """Home page rendering"""
    context = {
        "object_list": Breed.objects.all()[:3],
        "title": "PetPlace"
    }
    return render(request, 'dogs/index.html', context=context)


class BreedListView(ListView):
    """Displaying a list of breeds"""
    model = Breed
    extra_context = {
        "title": "All our breeds"
    }
    template_name = "dogs/breeds.html"
    paginate_by = 3


class BreedSearchListView(LoginRequiredMixin, ListView):
    """Searching dog by breed"""
    model = Breed
    template_name = "dogs/breeds.html"
    extra_context = {
        "title": "Search result"
    }

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Breed.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


class DogBreedListView(LoginRequiredMixin, ListView):
    """Rendering of dogs of the selected breed"""
    model = Dog
    template_name = "dogs/dogs.html"
    extra_context = {
        "title": "Dogs of the selected breed"
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get("pk"))
        return queryset


class DogListView(ListView):
    """Displaying a list of dogs"""
    model = Dog
    extra_context = {
        "title": "All our dogs"
    }
    template_name = "dogs/dogs.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    """Render of deactivated dogs"""
    model = Dog
    extra_context = {
        "title": "All our dogs"
    }
    template_name = "dogs/dogs.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """Searching dog by name"""
    model = Dog
    template_name = "dogs/dogs.html"
    extra_context = {
        "title": "Search result"
    }

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Dog.objects.filter(
            Q(name__icontains=query, is_active=True)
        )
        return object_list

class DogCreateView(LoginRequiredMixin, CreateView):
    """Rendering a page to create the dog"""
    model = Dog
    form_class = DogForm
    template_name = "dogs/create.html"
    extra_context = {
        "title": "Add dog"
    }
    success_url = reverse_lazy("dogs:dogs_list")
    
    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    """Show additional information about the dog"""
    model = Dog
    template_name = "dogs/detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data["title"] = f"All information {object_}"
        dog_object_increase = get_object_or_404(Dog, pk=object_.pk)
        if object_.owner != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            dog_object_increase.views_count()
        if object_.owner:
            object_owner_email = object_.owner.email
            if dog_object_increase.views % 10 == 0 and dog_object_increase.views != 0:
                send_views_email(dog_object_increase.name, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """Edit dog information"""
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


    def get_form_class(self):
        dog_forms = {
            UserRoles.ADMIN: DogAdminForm,
            UserRoles.MODERATOR: DogForm,
            UserRoles.USER: DogForm
        }

        user_role = self.request.user.role
        dog_form_class = dog_forms[user_role]
        return dog_form_class

    def get_success_url(self):
        return reverse("dogs:dog_detail", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """Rendering a page to delete the selected dog"""
    model = Dog
    template_name = "dogs/delete.html"
    success_url = reverse_lazy("dogs:dogs_list")
    permission_required = "dogs.delete_dog"
    permission_denied_message = "You have no rights"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data["title"] = f"Delete the {object_}"
        return context_data


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse("dogs:dogs_list"))