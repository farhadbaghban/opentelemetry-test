from django.urls import path
from .views import UserView

urlpatterns = [
    path("get/", UserView.as_view(), name="user-list"),
    path("get/<int:pk>/", UserView.as_view(), name="user-detail"),
]
