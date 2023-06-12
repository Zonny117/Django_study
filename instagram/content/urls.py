from django.urls import path
from content.views import UploadView, Profile, UploadReply

urlpatterns = [
    path("upload/", UploadView.as_view()),
    path("profile/", Profile.as_view()),
    path("reply/", UploadReply.as_view()),
]
