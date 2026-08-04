from rest_framework import serializers

from apps.accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "discord_id",
            "discord_username",
            "discord_avatar_url",
            "is_guild_member",
            "guild_roles",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
