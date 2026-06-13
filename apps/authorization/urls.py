from django.urls import path

from .views import DiscordLoginView

urlpatterns = [
    path(
        "discord/login/",
        DiscordLoginView.as_view(),
        name="discord-login",
    ),
]
