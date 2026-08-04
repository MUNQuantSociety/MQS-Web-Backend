# apps/authorization/services/discord.py

import requests
from django.conf import settings


class DiscordAPIError(Exception):
    pass


class DiscordClient:
    def __init__(self):
        self.base_url = settings.DISCORD["BASE_URL"]
        self.guild_id = settings.DISCORD["GUILD_ID"]
        self.bot_token = settings.DISCORD["BOT_TOKEN"]
        self.timeout = settings.DISCORD["REQUEST_TIMEOUT"]

    def get_guild_member(self, discord_user_id: str) -> dict:
        response = requests.get(
            f"{self.base_url}/guilds/{self.guild_id}/members/{discord_user_id}",
            headers={
                "Authorization": f"Bot {self.bot_token}",
            },
            timeout=self.timeout,
        )

        self._raise_for_discord_error(response)

        return response.json()

    def _raise_for_discord_error(self, response):
        if response.status_code < 400:
            return

        try:
            payload = response.json()
        except ValueError:
            payload = {
                "message": response.text,
            }

        raise DiscordAPIError(
            {
                "status_code": response.status_code,
                "discord_error": payload,
            }
        )
