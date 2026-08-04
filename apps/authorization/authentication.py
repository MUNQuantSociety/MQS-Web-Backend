# apps/authorization/authentication.py

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.accounts.models import Profile

_jwks_client = None


def _get_jwks_client() -> jwt.PyJWKClient:
    """Lazily builds a PyJWKClient against Supabase's JWKS endpoint.

    Supabase signs access tokens with an asymmetric key (ES256/RS256) rotated
    via its JWKS endpoint, not the legacy static HS256 secret.
    """
    global _jwks_client

    if _jwks_client is None:
        jwks_url = f"{settings.SUPABASE['URL']}/auth/v1/.well-known/jwks.json"
        _jwks_client = jwt.PyJWKClient(jwks_url)

    return _jwks_client


class SupabaseJWTAuthentication(BaseAuthentication):
    """Verifies a Supabase-issued access token and resolves it to a local Profile."""

    keyword = "Bearer"

    def authenticate(self, request):
        header = request.META.get("HTTP_AUTHORIZATION", "")

        if not header:
            return None

        parts = header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]

        try:
            signing_key = _get_jwks_client().get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
            )
        except jwt.PyJWTError as error:
            raise AuthenticationFailed(f"Invalid Supabase token: {error}")

        user_id = claims.get("sub")

        if not user_id:
            raise AuthenticationFailed("Supabase token is missing a subject claim")

        profile = self._sync_profile(user_id=user_id, claims=claims)

        return (profile, claims)

    def authenticate_header(self, request):
        return self.keyword

    def _sync_profile(self, user_id: str, claims: dict) -> Profile:
        metadata = claims.get("user_metadata") or {}

        discord_id = metadata.get("provider_id") or metadata.get("sub") or ""
        discord_username = (
            metadata.get("full_name")
            or metadata.get("name")
            or metadata.get("custom_claims", {}).get("global_name", "")
        )
        avatar_url = metadata.get("avatar_url") or metadata.get("picture") or ""
        email = claims.get("email") or metadata.get("email") or ""

        profile = Profile.objects.filter(id=user_id).first()

        if profile is None:
            if not discord_id:
                raise AuthenticationFailed(
                    "An account must be created by signing up with Discord first."
                )

            return Profile.objects.create(
                id=user_id,
                email=email,
                discord_id=discord_id,
                discord_username=discord_username,
                discord_avatar_url=avatar_url,
            )

        updates = {
            "email": email,
            "discord_id": discord_id,
            "discord_username": discord_username,
            "discord_avatar_url": avatar_url,
        }

        changed_fields = [
            field
            for field, value in updates.items()
            if value and getattr(profile, field) != value
        ]

        if changed_fields:
            for field in changed_fields:
                setattr(profile, field, updates[field])
            profile.save(update_fields=changed_fields + ["updated_at"])

        return profile
