from django.urls import path
from .views import hello, health


urlpatterns = [
    path("hello/", hello),
    path("health/", health),
]
