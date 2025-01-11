from django.urls import path
from .views import TripView

urlpatterns = [
    path("trips/", TripView.as_view(), name="trip-list"),
    path("trips/<uuid:trip_id>/", TripView.as_view(), name="trip-detail"),
]
