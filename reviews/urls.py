from django.urls import path
from .views import ReviewListView, ReviewDeactivatedListView
from .apps import ReviewsConfig
app_name = ReviewsConfig.name

urlpatterns = [
    path("", ReviewListView.as_view(), name="reviews_list"),
    path("deactivated/", ReviewDeactivatedListView.as_view(), name="reviews_deactivated_list"),
]