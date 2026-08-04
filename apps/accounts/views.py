from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import ProfileSerializer
from apps.authorization.services.discord import DiscordAPIError, DiscordClient


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(ProfileSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_discord(request):
    profile = request.user

    if not profile.discord_id:
        return Response(
            {
                "success": False,
                "message": "Profile has no linked Discord account",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    discord = DiscordClient()

    try:
        guild_member = discord.get_guild_member(discord_user_id=profile.discord_id)
    except DiscordAPIError as error:
        details = error.args[0] if error.args else {}
        if isinstance(details, dict) and details.get("status_code") == 404:
            profile.is_guild_member = False
            profile.guild_roles = []
            profile.save(update_fields=["is_guild_member", "guild_roles", "updated_at"])
            return Response(ProfileSerializer(profile).data)

        return Response(
            {
                "success": False,
                "message": "Failed to verify Discord guild membership",
                "error": details,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    profile.is_guild_member = True
    profile.guild_roles = guild_member.get("roles", [])
    profile.save(update_fields=["is_guild_member", "guild_roles", "updated_at"])

    return Response(ProfileSerializer(profile).data)
