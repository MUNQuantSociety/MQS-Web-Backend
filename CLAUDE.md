# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Django + Django REST Framework backend for MQS (a Discord-community-backed organization). Despite what `README.md` currently says (it describes an old FastAPI prototype and is stale — do not follow it), the project is Django. Entry point is `manage.py`, settings live in `config/settings/`.

Auth model: the frontend handles Discord OAuth via **Supabase Auth**; this backend never talks OAuth directly. Instead it verifies the Supabase-issued JWT on each request and mirrors relevant claims into a local `Profile`. Discord's own API (bot token) is only used server-side to check guild membership/roles, via `apps/authorization/services/discord.py`.

## Commands

Windows/PowerShell, using the local venv:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python manage.py runserver
python manage.py migrate
python manage.py makemigrations <app_label>
python manage.py createsuperuser

# Tests (plain Django test runner — no pytest is installed)
python manage.py test
python manage.py test apps.accounts
python manage.py test tests.test_accounts
python manage.py test apps.accounts.tests.SomeTestCase.test_something
```

`manage.py` hardcodes `DJANGO_SETTINGS_MODULE=config.settings.local` as the default. There's no override in the codebase for other environments — production deploys must set `DJANGO_SETTINGS_MODULE=config.settings.production` explicitly in the process environment.

Config is loaded from a `.env` file at the repo root via `python-decouple`; copy `.env.example` to `.env` before running anything. Required (no default) keys: `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`, `DISCORD_GUILD_ID`, `DISCORD_BOT_TOKEN`, `SUPABASE_URL` — `config/settings/base.py` will raise at import time if any of these are missing.

## Architecture

**Settings split**: `config/settings/base.py` holds everything shared; `local.py` and `production.py` each do `from .base import *` and layer on env-specific overrides (debug flags, HSTS/cookie security, email backend). Add new settings to `base.py` unless they're genuinely environment-specific.

**App layout** (`apps/`, all registered under `apps.<name>` in `INSTALLED_APPS`):
- `api` — root router only. `config/urls.py` mounts everything under `/api/v1/` via `apps/api/urls.py`, which in turn includes each app's own `urls.py` (e.g. `auth/` → `apps.authorization.urls`, `accounts/` → `apps.accounts.urls`). New apps get wired in here, not in `config/urls.py`.
- `accounts` — the `Profile` model (local mirror of a Supabase `auth.users` row, PK = Supabase UUID) plus `me/` and `sync-discord/` endpoints.
- `authorization` — no models; holds cross-cutting auth pieces: `authentication.py` (`SupabaseJWTAuthentication`, registered as the sole DRF `DEFAULT_AUTHENTICATION_CLASSES`) and `services/discord.py` (`DiscordClient`, a thin wrapper over the Discord bot REST API for guild membership lookups). This app is mid-refactor on the current branch (`views.py`/`serializers.py` are currently stubs; a prior `services/discord_auth.py` was removed in favor of `services/discord.py`).
- `calendar`, `ibkr`, `leaderboard`, `backtests`, `resources`, `insights` — scaffolded (models/services/urls/views files exist but are placeholders), reserved for future domain logic. Each follows the same `models.py` / `services.py` (business logic / external calls) / `views.py` (thin DRF view functions) / `urls.py` split — follow that pattern when filling one in.

**Request auth flow**: every request runs through `SupabaseJWTAuthentication.authenticate()` (`apps/authorization/authentication.py`). It reads `Authorization: Bearer <token>`, verifies it as an ES256/RS256 JWT against Supabase's JWKS endpoint (`{SUPABASE_URL}/auth/v1/.well-known/jwks.json`, fetched via `PyJWKClient`) with `audience="authenticated"`, then `get_or_create`s/updates a `Profile` from the token's `sub` and `user_metadata` claims (Discord id/username/avatar/email). The returned `Profile` becomes `request.user`. DRF's default permission class is `AllowAny`, so views must opt into `@permission_classes([IsAuthenticated])` themselves — auth alone does not gate access. (There is no static `SUPABASE_JWT_SECRET` — Supabase projects on the newer asymmetric-key model don't issue HS256 tokens, so verification must go through the JWKS endpoint.)

**Discord guild sync is separate from login**: `POST /api/v1/accounts/sync-discord/` (`apps/accounts/views.py`) explicitly calls `DiscordClient.get_guild_member()` using the bot token to refresh `Profile.is_guild_member` / `Profile.guild_roles`. This is not run automatically on every authenticated request — call it when guild membership/roles need to be current.

**Top-level `tests/`**: mirrors app names (`tests/test_accounts.py`, etc.) but is currently placeholder-only; real tests for an app can also live in that app's own `tests.py` (e.g. `apps/accounts/tests.py`). Both are picked up by `manage.py test`.

## Working on the current branch (`feat/discord-auth`)

The `authorization` app is actively being restructured: `services/discord_auth.py` was deleted in favor of `services/discord.py`, and `views.py`/`serializers.py` in that app are stubbed pending being wired up to `accounts`. Check `git status`/`git diff` before assuming those files are dead — they're mid-edit, not unused.
