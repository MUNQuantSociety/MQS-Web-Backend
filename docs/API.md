# API Reference

Base URL: `/api/v1/`

All endpoints go through `SupabaseJWTAuthentication` (`apps/authorization/authentication.py`), which reads an `Authorization: Bearer <token>` header if present and verifies it as a Supabase-issued JWT. Endpoints marked **Auth required** additionally use `@permission_classes([IsAuthenticated])` and will return `401 Unauthorized` without a valid token. Endpoints not marked as such are publicly accessible even though the token, if sent, is still verified and attached as `request.user`.

---

## Health

### `GET /api/v1/health/`
No auth required.

Liveness check.

**Response `200`**
```json
{ "status": "ok" }
```

---

## Accounts (`/api/v1/accounts/`)

Source: `apps/accounts/views.py`, `apps/accounts/serializers.py`

### `GET /api/v1/accounts/me/`
**Auth required**

Returns the authenticated user's `Profile`.

**Response `200`**
```json
{
  "id": "uuid",
  "email": "string",
  "discord_id": "string",
  "discord_username": "string",
  "discord_avatar_url": "string",
  "is_guild_member": true,
  "guild_roles": ["role_id", "..."],
  "has_password": true,
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

### `POST /api/v1/accounts/confirm-password-set/`
**Auth required**

Marks the authenticated user's profile as having a password set (`has_password = true`). Takes no request body.

**Response `200`** — updated `Profile`, same shape as `me/`.

### `POST /api/v1/accounts/sync-discord/`
**Auth required**

Refreshes Discord guild membership and roles for the authenticated user by calling the Discord bot API (`DiscordClient.get_guild_member`, `apps/authorization/services/discord.py`). Not run automatically — call this when membership/roles need to be current. Takes no request body.

**Response `200`** — updated `Profile`, same shape as `me/`.

**Response `400`** — profile has no linked Discord account:
```json
{ "success": false, "message": "Profile has no linked Discord account" }
```

**Response `502`** — Discord API call failed for a reason other than "not a member":
```json
{
  "success": false,
  "message": "Failed to verify Discord guild membership",
  "error": { "status_code": 0, "discord_error": {} }
}
```

Note: if Discord returns `404` (user not found in the guild), this is treated as a normal outcome, not an error — the profile is updated with `is_guild_member: false`, `guild_roles: []`, and a `200` is returned.

---

## Placeholder endpoints

These apps are scaffolded but not yet implemented. Their views return static/canned data with no auth and no real logic. Do not build against these as if they were final.

| Method | Path | Response |
|---|---|---|
| `GET` | `/api/v1/backtests/status/` | `{ "status": "ok" }` |
| `GET` | `/api/v1/calendar/events/` | `{ "events": [] }` |
| `GET` | `/api/v1/ibkr/status/` | `{ "status": "ok" }` |
| `GET` | `/api/v1/leaderboard/top/` | `{ "leaders": [] }` |

`apps/authorization`, `apps/resources`, and `apps/insights` currently register no URLs at all (`urlpatterns = []`).

---

## Authentication details

See `apps/authorization/authentication.py`. Summary:

- Frontend does Discord OAuth via Supabase Auth; this backend never talks OAuth directly.
- Each request's JWT is verified (ES256/RS256, `audience="authenticated"`) against Supabase's JWKS endpoint.
- On success, a local `Profile` is `get_or_create`d/updated from the token's `sub` and `user_metadata` (Discord id/username/avatar/email), and set as `request.user`.
- DRF's default permission class is `AllowAny` — a valid token alone does not restrict access; each view opts into `IsAuthenticated` explicitly.

---

*This file is maintained by hand. When adding or changing an endpoint, update this doc in the same change.*
