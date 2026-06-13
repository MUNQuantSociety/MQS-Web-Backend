# apps/authorization/services/discord.py

import requests
from django.conf import settings


class DiscordAPIError(Exception):
    pass


class DiscordClient:
    def __init__(self):
        self.base_url = settings.DISCORD["BASE_URL"]
        self.client_id = settings.DISCORD["CLIENT_ID"]
        self.client_secret = settings.DISCORD["CLIENT_SECRET"]
        self.guild_id = settings.DISCORD["GUILD_ID"]
        self.bot_token = settings.DISCORD["BOT_TOKEN"]
        self.timeout = settings.DISCORD["REQUEST_TIMEOUT"]

    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        response = requests.post(
            f"{self.base_url}/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            auth=(
                self.client_id,
                self.client_secret,
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=self.timeout,
        )

        self._raise_for_discord_error(response)

        return response.json()

    def get_current_user(self, access_token: str) -> dict:
        response = requests.get(
            f"{self.base_url}/users/@me",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            timeout=self.timeout,
        )

        self._raise_for_discord_error(response)

        return response.json()

    def get_guild_member(self, discord_user_id: str) -> dict:
        response = requests.get(
            f"""
                {self.base_url}/guilds/{self.guild_id}/members/{discord_user_id}
            """,

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
