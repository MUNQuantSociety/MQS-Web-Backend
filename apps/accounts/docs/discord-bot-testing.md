# Test bot

Copy id of user
Copy discord guild id also
Copy discord bot token

Include all in your .env

# Api reference
docs: https://docs.discord.com/developers/reference

## Baseurl:
https://discord.com/api

version:
https://discord.com/api/v{version_number}

## Get Guild Member
https://docs.discord.com/developers/resources/guild#get-guild-member

{baseurl}/guilds/{guild.id}/members/{user.id};

### response object
https://docs.discord.com/developers/resources/guild#guild-member-object
{
  "user": {},
  "nick": "NOT API SUPPORT",
  "avatar": null,
  "banner": null,
  "roles": [],
  "joined_at": "2015-04-26T06:26:56.936000+00:00",
  "deaf": false,
  "mute": false
}

## Get role
https://docs.discord.com/developers/resources/guild#get-guild-role

- roles
{baseurl}/guilds/{guild.id}/roles
- single role
{baseurl}/guilds/{guild.id}/roles/{role.id};

### response object
{
  "id": "41771983423143936",
  "name": "WE DEM BOYZZ!!!!!!",
  "color": 3447003,
  "colors": {
    "primary_color": 3447003,
    "secondary_color": null,
    "tertiary_color": null
  },
  "hoist": true,
  "icon": "cf3ced8600b777c9486c6d8d84fb4327",
  "unicode_emoji": null,
  "position": 1,
  "permissions": "66321471",
  "managed": false,
  "mentionable": false,
  "flags": 0
}
