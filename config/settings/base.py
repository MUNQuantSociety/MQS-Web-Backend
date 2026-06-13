from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parents[2]

SECRET_KEY = config("DJANGO_SECRET_KEY", default="unsafe-secret-key")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
# Usage:
# from django.conf import settings
#
# PROJECT_DIR = settings.BASE_DIR
# SECRET_KEY = settings.SECRET_KEY
# DEBUG = settings.DEBUG


# =========================================================
# Discord Environment Config
# =========================================================

DISCORD = {
    "BASE_URL": config(
        "DISCORD_BASE_URL",
        default="https://discord.com/api/v10",
    ),

    "CLIENT_ID": config(
        "DISCORD_CLIENT_ID",
    ),

    "CLIENT_SECRET": config(
        "DISCORD_CLIENT_SECRET",
    ),

    "GUILD_ID": config(
        "DISCORD_GUILD_ID",
    ),

    "BOT_TOKEN": config(
        "DISCORD_BOT_TOKEN",
    ),

    "REQUEST_TIMEOUT": config(
        "DISCORD_REQUEST_TIMEOUT",
        default=10,
        cast=int,
    ),

    "REDIRECT_URI": config(
        "DISCORD_REDIRECT_URI",
        default="http://localhost:8080/callback",
    ),

    "TEST_USER": config(
        "DISCORD_TEST_USER",
        default="",
    ),
}

# Usage:
#
# from django.conf import settings
#
# DISCORD_BASE_URL = settings.DISCORD["BASE_URL"]
# DISCORD_GUILD_ID = settings.DISCORD["GUILD_ID"]
# DISCORD_BOT_TOKEN = settings.DISCORD["BOT_TOKEN"]
# DISCORD_TEST_USER = settings.DISCORD["TEST_USER"]


ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=Csv(),
)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]
LOCAL_APPS = [
    "apps.api",
    "apps.accounts",
    "apps.authorization",
    "apps.calendar",
    "apps.ibkr",
    "apps.leaderboard",
    "apps.backtests",
    "apps.resources",
    "apps.insights",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DB_ENGINE = config("DJANGO_DB_ENGINE", default="django.db.backends.sqlite3")
DB_NAME = config("DJANGO_DB_NAME", default="db.sqlite3")

if DB_ENGINE == "django.db.backends.sqlite3":
    db_path = Path(DB_NAME)
    if not db_path.is_absolute():
        DB_NAME = str((BASE_DIR / db_path).resolve())

DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "NAME": DB_NAME,
    }
}

if DB_ENGINE != "django.db.backends.sqlite3":
    DATABASES["default"].update(
        {
            "USER": config("DJANGO_DB_USER", default=""),
            "PASSWORD": config("DJANGO_DB_PASSWORD", default=""),
            "HOST": config("DJANGO_DB_HOST", default=""),
            "PORT": config("DJANGO_DB_PORT", default=""),
        }
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
