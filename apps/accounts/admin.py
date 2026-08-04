from django.contrib import admin

from apps.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "discord_username",
        "discord_id",
        "email",
        "is_guild_member",
        "updated_at",
    )
    search_fields = ("discord_username", "discord_id", "email")
    list_filter = ("is_guild_member",)
