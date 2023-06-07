from django.urls import path
from content.views import UploadView

urlpatterns = [
    path("upload/", UploadView.as_view()),
]
