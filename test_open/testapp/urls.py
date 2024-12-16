from django.urls import path
from .views import UserView
urlpatterns = [
    path("get/",UserView.as_view())
]
