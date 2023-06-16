from django.contrib import admin
from django.urls import path
from .views import Main, Upload


urlpatterns = [
    path("", Main.as_view()),
    path("upload/", Upload.as_view()),
]
