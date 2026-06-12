import os
import json
import requests

from load_env import load_env

# =========================================================
# Paths
# =========================================================

BASE_DIR = os.path.dirname(__file__)

ROLE_MAPPING_FILE = os.path.join(
    BASE_DIR,
    "role_mapping.json"
)

INTERNAL_ROLE_FILE = os.path.join(
    BASE_DIR,
    "internal_roles.json"
)

# =========================================================
# Local Env
# =========================================================

env = load_env(
    os.path.join(BASE_DIR, ".env.discord")
)

# =========================================================
# Config
# =========================================================

DEBUG = env.get(
    "DEBUG",
    "False"
) == "True"

DISCORD_BASE_URL = env.get(
    "DISCORD_BASE_URL"
)

DISCORD_GUILD_ID = env.get(
    "DISCORD_GUILD_ID"
)

DISCORD_BOT_TOKEN = env.get(
    "DISCORD_BOT_TOKEN"
)

DISCORD_TEST_USER = env.get(
    "DISCORD_TEST_USER"
)

REQUEST_TIMEOUT = int(
    env.get(
        "REQUEST_TIMEOUT",
        10
    )
)
print("DEBUG:", DEBUG)

headers = {
    "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
}


# =========================================================
# RESPONSE HELPERS
# =========================================================

def success_response(msg="", data=None):
    return {
        "success": True,
        "msg": msg,
        "data": data
    }


def error_response(
    msg="Something went wrong",
    error_code="UNKNOWN_ERROR",
    error=None,
    status_code=500
):
    response = {
        "success": False,
        "msg": msg,
        "error_code": error_code,
        "status_code": status_code
    }

    if DEBUG and error:
        response["error"] = error

    return response


# =========================================================
# EXTERNAL API ERROR HELPERS
# =========================================================

def discord_error(response):
    try:
        error_json = response.json()

        return error_response(
            msg=error_json.get("message", "Discord API Error"),
            error_code=f"DISCORD_{response.status_code}",
            error=error_json,
            status_code=response.status_code
        )

    except Exception:
        return error_response(
            msg="Discord API Error",
            error_code=f"DISCORD_{response.status_code}",
            error=response.text,
            status_code=response.status_code
        )


# =========================================================
# JSON FILE HELPERS
# =========================================================

def load_json_file(path, default=None):
    if default is None:
        default = []

    if not os.path.exists(path):
        return default

    with open(path, "r") as file:
        return json.load(file)


def save_json_file(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


# =========================================================
# INTERNAL ROLE HELPERS
# =========================================================

def create_internal_role(name):
    roles = load_json_file(INTERNAL_ROLE_FILE)

    role = {
        "id": str(uuid.uuid4()),
        "name": name
    }

    roles.append(role)

    save_json_file(INTERNAL_ROLE_FILE, roles)

    return role


def create_role_mapping(discord_role_id, internal_role):
    mappings = load_json_file(ROLE_MAPPING_FILE)

    mappings.append({
        "discord_role_id": discord_role_id,
        "internal_role_id": internal_role["id"]
    })

    save_json_file(ROLE_MAPPING_FILE, mappings)

    return success_response(
        "Role mapping created"
    )


def mapping_exists(discord_role_id):
    mappings = load_json_file(ROLE_MAPPING_FILE)

    for mapping in mappings:
        if mapping["discord_role_id"] == discord_role_id:
            return True

    return False


# =========================================================
# DISCORD SERVICES
# =========================================================

def get_discord_roles_and_create_internal_role_map():
    endpoint = f"/guilds/{DISCORD_GUILD_ID}/roles"

    try:
        response = requests.get(
            f"{DISCORD_BASE_URL}{endpoint}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

    except requests.RequestException as e:
        return error_response(
            msg="Failed to communicate with Discord",
            error_code="DISCORD_CONNECTION_ERROR",
            error=str(e)
        )

    if response.status_code != 200:
        return discord_error(response)

    discord_roles = response.json()

    for discord_role in discord_roles:

        if discord_role["name"] == "@everyone":
            continue

        if discord_role["managed"]:
            continue

        if mapping_exists(discord_role["id"]):
            continue

        internal_role = create_internal_role(
            name=discord_role["name"]
        )

        create_role_mapping(
            discord_role_id=discord_role["id"],
            internal_role=internal_role
        )

    return success_response(
        msg="Role sync complete"
    )


# def get_discord_user(user_id=None):
#
#     if not user_id:
#         return error_response(
#             msg="User ID is required",
#             error_code="INVALID_PARAMS",
#             status_code=400
#         )
#
#     try:
#         response = requests.get(
#             f"{DISCORD_BASE_URL}/guilds/{DISCORD_GUILD_ID}/members/{user_id}",
#             headers=headers,
#             timeout=REQUEST_TIMEOUT
#         )
#
#     except requests.RequestException as e:
#         return error_response(
#             msg="Failed to communicate with Discord",
#             error_code="DISCORD_CONNECTION_ERROR",
#             error=str(e)
#         )
#
#     if response.status_code != 200:
#         return discord_error(response)
#
#     return success_response(
#         msg="User fetched successfully",
#         data=response.json()
#     )


# Function: get userid from token
def get_discord_user(token):
    if not token:
        return error_response(
            msg="Token must be present to get userID",
            error_code="INVALID_PARAMS",
            status_code=400
        )

    try:
        response = requests.get(
            f"{DISCORD_BASE_URL}/user/@me",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=REQUEST_TIMEOUT
        )

        return response

    except requests.RequestException as e:
        return error_response(
            msg="Failed to get discord user",
            error_code="DISCORD_ERROR",
            error=str(e)
        )


# =========================================================
# USER FLOW
# =========================================================
"""
@params: access_token (use the token to send to DISCORD_API/user/me)
that get's the user id
"""


# def create_user_via_discord(token):
#
#     user_response = get_discord_user(token)
#
#     if not user_response["success"]:
#         return error_response(
#             msg=user_response["msg"],
#             error_code=user_response["error_code"],
#             error=user_response.get("error"),
#             status_code=user_response["status_code"]
#         )
#
#     discord_user = user_response["data"]
#
#     return success_response(
#         msg="Discord user processed successfully",
#         data={
#             "discord_user": discord_user
#         }
#     )


# =========================================================
# TEST
# =========================================================

# print(
#     json.dumps(
#         # create_user_via_discord("FAKEACCESSTOKEN1234"),
#         indent=4
#     )
# )
print(get_discord_user("a"))
