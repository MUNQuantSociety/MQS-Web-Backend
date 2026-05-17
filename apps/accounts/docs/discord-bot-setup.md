# Discord Bot Setup

================================================================================
Author: Skills Nwokolo Anthony
Role: Authentication / Infrastructure
Version: 1.0.0
Last Updated: 2026-05-06
================================================================================

## Purpose

This bot is not designed as a traditional Discord bot.

It currently exists to support backend infrastructure for:

- guild membership verification
- role retrieval
- Discord identity validation

The backend communicates directly with Discord's REST API using the bot token.

Current architecture:

```text
Frontend
    ↓
Django Backend
    ↓
Discord REST API
    ↓
Guild Membership + Roles
```

The bot is intentionally minimal and read-only.

---

# Developer Portal

Create and manage the bot here:

https://discord.com/developers/applications

---

# Authorization Flow

## Public Bot

Currently left enabled due to Discord install configuration
requirements.

This does not affect backend security because:
- the bot token remains private
- permissions are minimal
- the bot is read-only

---

## Requires OAuth2 Code Grant

| Setting                    | Value |
|----------------------------|-------|
| Requires OAuth2 Code Grant | OFF   |

### Reason

Not needed for the current architecture.

The backend handles:
- authentication
- token exchange
- guild verification

Enabling this adds unnecessary OAuth complexity.

---

# Gateway Intents

## Presence Intent

| Setting         | Value |
|-----------------|-------|
| Presence Intent | OFF   |

### Reason

Presence tracking is not required.

The system does not use:
- online status
- activities
- streaming state
- idle state

---

## Server Members Intent

| Setting               | Value |
|-----------------------|-------|
| Server Members Intent | ON    |

### Reason

This is the most important setting.

Required for reliable:
- guild member lookup
- role retrieval
- membership verification

Without this intent:
- member APIs become unreliable
- guild member access may fail

The backend depends on this.

---

## Message Content Intent

| Setting                | Value |
|------------------------|-------|
| Message Content Intent | OFF   |

### Reason

The bot does not read messages.

Not needed for:
- moderation
- commands
- AI responses
- chat interactions

---

# Bot Permissions

## Current Permission Model

The bot is intentionally low privilege.

It does NOT currently:
- manage roles
- moderate users
- manage channels
- send messages
- use slash commands

---

## Required Permissions

| Permission    | Value |
|---------------|-------|
| View Channels | ON    |

### Reason

Minimal baseline permission.

Allows the bot to:
- properly exist within the guild
- access guild visibility metadata
- interact reliably with guild APIs

---

# Important Distinction

Permissions and intents are different things.

```text
Permissions
    → what the bot can do

Gateway Intents
    → what Discord allows the bot to access
```

For this architecture:

```text
Server Members Intent
    >
Most bot permissions
```

The backend relies more on intents than elevated permissions.

---

# Security Model

The bot should remain read-only unless new infrastructure requires otherwise.

Rule:

```text
Do not grant permissions until a feature requires them.
```

This keeps:
- attack surface small
- infrastructure easier to reason about
- server risk low

---

#  Add bot to your server

Go to:

```text id="wjlwmr"
OAuth2
    ↓
URL Generator
```

---

# Scopes

Select:

```text id="n48o0m"
[x] bot
```

That tells Discord:

```text id="wjlwmm"
"Install this bot into a guild/server."
```

---

# Bot Permissions

Select ONLY:

```text id="3cjlwm"
[x] View Channels
```

Nothing else for now.

---

# Generated URL

Discord generates an invite URL at the bottom.

Open it in browser.

---

# Then

Discord will ask:

```text id="jlwm5p"
"Which server do you want to add this bot to?"
```

Choose your server.

Approve.

Done.

---

# After Installation

Your bot now:

* exists inside the guild,
* has guild access,
* can participate in member lookup,
* can retrieve roles through your backend.

---

# Current MVP Scope

Current backend responsibilities:
- verify Discord identity
- verify guild membership
- retrieve member roles
- map Discord roles to backend permissions

The backend does NOT currently:
- run a websocket bot
- listen for events
- process Discord messages
- maintain realtime synchronization

Discord is currently being used as:
- an identity provider
- a permission source
- a guild membership provider
