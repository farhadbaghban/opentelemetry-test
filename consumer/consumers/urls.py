from django.urls import path
from .views import ReqRes

urlpatterns = [
    path("retrieve/", ReqRes.as_view()),
]
