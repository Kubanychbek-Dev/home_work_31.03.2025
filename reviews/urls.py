from django.urls import path
from .views import (ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView,
                    ReviewUpdateView, ReviewDeleteView, review_toggle_activity)

from .apps import ReviewsConfig
app_name = ReviewsConfig.name

urlpatterns = [
    path("", ReviewListView.as_view(), name="reviews_list"),
    path("deactivated/", ReviewDeactivatedListView.as_view(), name="reviews_deactivated_list"),
    path("create/", ReviewCreateView.as_view(), name="review_create"),
    path("detail/<slug:slug>/", ReviewDetailView.as_view(), name="review_detail"),
    path("update/<slug:slug>/", ReviewUpdateView.as_view(), name="review_update"),
    path("deactivated/<slug:slug>/", ReviewDeleteView.as_view(), name="review_delete"),
    path("toggle/<slug:slug>/", review_toggle_activity, name="review_toggle"),
]
