"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.contrib.messages import constants as message_constants
from envparse import Env


env = Env(
    SECRET_KEY=str,
    ALLOWED_HOSTS=dict(cast=list, subcast=str, default=[]),
    TIME_ZONE=dict(cast=str, default="Europe/Budapest"),
    LANGUAGE_CODE=dict(cast=str, default="en-us"),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party apps
    "constance",
    "constance.backends.database",
    "crispy_forms",
    "widget_tweaks",
    # custom apps
    "slackbot.apps.SlackbotConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "string_if_invalid": "HIBA",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "slackbot.context_processors.is_bot_paused",
                "slackbot.context_processors.slack_button",
            ],
        },
    }
]

WSGI_APPLICATION = "web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "..", "data", "db.sqlite3"),
    }
}

CACHES = {"default": {"BACKEND": "uwsgicache.UWSGICache", "LOCATION": "channels"}}

# This is needed so you can start the shell... because from there you can't access uWSGI
# this will fall back to django.core.cache.backends.locmem.LocMemCache
UWSGI_CACHE_FALLBACK = True

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = env("LANGUAGE_CODE")
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "..", "static_root")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

CRISPY_TEMPLATE_PACK = "bootstrap3"

# bootstrap CSS classes
MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-info",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-danger",
}

BOT_ACCESS_TOKEN_DEFAULT = "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx"

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "SLACK_CLIENT_ID": (
        "xxxxxxxxxxxx.xxxxxxxxxxxx",
        "Slack client id from slack website",
    ),
    "SLACK_CLIENT_SECRET": (
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "Slack client secret from slack website",
    ),
    "SLACK_REDIRECT_URI": (" http://website/redirect-url", "Redirect url"),
    "GERRIT_URL": ("https://gerrit.instance.url", "main URL for gerrit instance"),
    "ACCESS_TOKEN": (
        "xoxp-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "User access token got from OAuth flow. Starts with xoxp-",
    ),
    "SCOPE": ("identify,bot,commands", "Scope got after OAuth redirect"),
    "USER_ID": (
        "UXXXXXXXX",
        "Slack user ID who installed slackbot to the Slack workspace",
    ),
    "TEAM_NAME": ("Workspace", "Slack workspace the slackbot is installed to"),
    "TEAM_ID": ("TXXXXXXXX", "Slack team ID where the bot is installed to"),
    "BOT_USER_ID": ("UXXXXXXXX", "Slack bot user ID"),
    "BOT_ACCESS_TOKEN": (
        BOT_ACCESS_TOKEN_DEFAULT,
        "Slack bot access token. Starts with xoxb-",
    ),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Slack client": ("SLACK_CLIENT_ID", "SLACK_CLIENT_SECRET", "SLACK_REDIRECT_URI"),
    "Slack permissions": ("BOT_USER_ID", "BOT_ACCESS_TOKEN", "SCOPE", "ACCESS_TOKEN"),
    "Gerrit": ("GERRIT_URL",),
    "Slack good to know": ("USER_ID", "TEAM_NAME", "TEAM_ID"),
}
