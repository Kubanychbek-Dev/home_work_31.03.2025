from django.urls import path
from .apps import DogsConfig
from .views import index_view

app_name = DogsConfig.name


urlpatterns = [
    path('', index_view, name='index')
]