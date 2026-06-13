# apps/authorization/services/discord_auth.py

from apps.authorization.services.discord import DiscordClient


def login_with_discord(code: str, redirect_uri: str):
    discord = DiscordClient()

    token_data = discord.exchange_code(
        code=code,
        redirect_uri=redirect_uri,
    )

    access_token = token_data["access_token"]

    discord_user = discord.get_current_user(
        access_token=access_token,
    )

    guild_member = discord.get_guild_member(
        discord_user_id=discord_user["id"],
    )

    # TODO: Create user
    # user = create_via_discord(
    #     discord_user=discord_user,
    #     guild_member=guild_member,
    # )

    return {
        "discord_user": discord_user,
        "guild_member": guild_member,
    }
