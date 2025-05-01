from django.urls import path
from .apps import DogsConfig
from .views import (index_view, BreedListView, DogBreedListView, DogListView,
                    DogCreateView, DogDetailView, DogUpdateView, DogDeleteView)

app_name = DogsConfig.name


urlpatterns = [
    path('', index_view, name='index'),
    path('breeds/', BreedListView.as_view(), name='breeds'),
    path('breeds/<int:pk>/dogs/', DogBreedListView.as_view(), name='breed_dogs'),
    path('dogs/', DogListView.as_view(), name='dogs_list'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/update/<int:pk>/', DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='dog_delete'),
]