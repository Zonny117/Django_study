from django.urls import path
from content.views import UploadView, Profile

urlpatterns = [
    path("upload/", UploadView.as_view()),
    path("profile/", Profile.as_view()),
]
