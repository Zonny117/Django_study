from django.urls import path
from content.views import UploadView, Profile, UploadReply, ToggelLike, ToggelBookmark

urlpatterns = [
    path("upload/", UploadView.as_view()),
    path("profile/", Profile.as_view()),
    path("reply/", UploadReply.as_view()),
    path("like/", ToggelLike.as_view()),
    path("bookmark/", ToggelBookmark.as_view()),
]
