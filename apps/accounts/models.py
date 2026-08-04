import uuid

from django.db import models


class Profile(models.Model):
    """App-local profile keyed by the Supabase auth.users UUID."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    email = models.EmailField(blank=True, default="")
    discord_id = models.CharField(max_length=32, blank=True, default="")
    discord_username = models.CharField(max_length=255, blank=True, default="")
    discord_avatar_url = models.URLField(blank=True, default="")

    is_guild_member = models.BooleanField(default=False)
    guild_roles = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.discord_username or str(self.id)
