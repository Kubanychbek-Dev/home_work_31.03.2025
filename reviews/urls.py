from django.urls import path
from .views import ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView

from .apps import ReviewsConfig
app_name = ReviewsConfig.name

urlpatterns = [
    path("", ReviewListView.as_view(), name="reviews_list"),
    path("deactivated/", ReviewDeactivatedListView.as_view(), name="reviews_deactivated_list"),
    path("create/", ReviewCreateView.as_view(), name="review_create"),
    path("detail/", ReviewDetailView.as_view(), name="review_detail"),
    path("update/", ReviewUpdateView.as_view(), name="review_update"),
    path("deactivated/", ReviewDeleteView.as_view(), name="review_delete"),
]