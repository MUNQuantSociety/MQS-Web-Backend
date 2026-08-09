import uuid
from typing import cast

import jwt
from django.conf import settings
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.accounts.models import Profile


def make_token(user_id, **metadata):
    payload = {
        "sub": str(user_id),
        "aud": "authenticated",
        "email": "member@example.com",
        "user_metadata": {
            "provider_id": "123456789012345678",
            "full_name": "Test Member",
            "avatar_url": "https://cdn.discordapp.com/avatars/123/abc.png",
            **metadata,
        },
    }
    return jwt.encode(payload, settings.SUPABASE["JWT_SECRET"], algorithm="HS256")


class SupabaseJWTAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_me_without_token_is_unauthorized(self):
        response = self.client.get("/api/v1/accounts/me/")
        self.assertEqual(response.status_code, 401)

    def test_me_with_invalid_token_is_unauthorized(self):
        cast(APIClient, self.client).credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")
        response = self.client.get("/api/v1/accounts/me/")
        self.assertEqual(response.status_code, 401)

    def test_me_with_valid_token_creates_and_returns_profile(self):
        user_id = uuid.uuid4()
        token = make_token(user_id)

        cast(APIClient, self.client).credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = cast(Response, self.client.get("/api/v1/accounts/me/"))

        self.assertEqual(response.status_code, 200)
        assert response.data is not None
        self.assertEqual(response.data["id"], str(user_id))
        self.assertEqual(response.data["discord_id"], "123456789012345678")
        self.assertTrue(Profile.objects.filter(id=user_id).exists())
