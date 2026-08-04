from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("me/", views.me, name="me"),
    path("sync-discord/", views.sync_discord, name="sync-discord"),
]
