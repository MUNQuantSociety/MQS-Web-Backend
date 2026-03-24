from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("upload/", views.upload_file, name="upload-file"),
]
