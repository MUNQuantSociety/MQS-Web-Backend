"""Project URL configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("calendar/", include("apps.calendar.urls")),
    path("ibkr/", include("apps.ibkr.urls")),
    path("leaderboard/", include("apps.leaderboard.urls")),
    path("backtests/", include("apps.backtests.urls")),
    path("resources/", include("apps.resources.urls")),
    path("insights/", include("apps.insights.urls")),
]
