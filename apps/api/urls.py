from django.urls import include, path

from . import views

app_name = "api"

urlpatterns = [
    path("health/", views.health_check, name="health-check"),

    path("auth/", include("apps.authorization.urls")),
]
