from django.urls import path

from . import views

app_name = "backtests"

urlpatterns = [
    path("status/", views.status, name="status"),
]
