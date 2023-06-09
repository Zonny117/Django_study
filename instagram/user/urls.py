from django.urls import path
from .views import Join, Login, Logout, UploadProfileImage

urlpatterns = [
    path("join/", Join.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("profile/upload/", UploadProfileImage.as_view()),
]
