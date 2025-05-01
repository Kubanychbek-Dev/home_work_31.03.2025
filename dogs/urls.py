from django.urls import path
from .apps import DogsConfig
from django.views.decorators.cache import cache_page, never_cache

from .views import (index_view, BreedListView, DogBreedListView, DogListView,
                    DogCreateView, DogDetailView, DogUpdateView, DogDeleteView)

app_name = DogsConfig.name


urlpatterns = [
    path('', index_view, name='index'),
    path('breeds/', cache_page(30)(BreedListView.as_view()), name='breeds'),
    path('breeds/<int:pk>/dogs/', DogBreedListView.as_view(), name='breed_dogs'),
    path('dogs/', cache_page(30)(DogListView.as_view()), name='dogs_list'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='dog_update'),
    path('dogs/delete/<int:pk>/', never_cache(DogDeleteView.as_view()), name='dog_delete'),
]