from os import environ as env
from pathlib import Path
from typing import Literal

from django.utils.log import DEFAULT_LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "this-generates-static-files-so-the-secret-key-doesn't-matter"

DEBUG: bool = env.get("DEBUG", "0").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = ["*"]  # here again, that Django app is not meant to be deployed anyway
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_tailwind_cli",
    "django_google_fonts",
    "myresume",
]
if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = []
if DEBUG:
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
        "myresume.middlewares.TOMLCacheClearingMiddleware",
    ]

ROOT_URLCONF = "myresume.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "myresume.context_processors.resume_lang",
                "myresume.context_processors.root_path",
            ],
        },
    },
]

WSGI_APPLICATION = "myresume.wsgi.application"

DATABASES = {}  # type: ignore [var-annotated]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env.get("STATIC_URL", "static/")
STATICFILES_DIRS = [BASE_DIR / "myresume" / "staticfiles"]
STATIC_ROOT = BASE_DIR / "dist" / "static"
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    }
}

# Logging
# https://docs.djangoproject.com/en/5.0/ref/logging/

LOGGING = DEFAULT_LOGGING.copy()
LOGGING["loggers"]["myresume"] = {
    "handlers": ["console"],
    "level": "DEBUG" if DEBUG else "INFO",
}

# Tailwind CSS
# https://django-tailwind-cli.andrich.me/settings/

TAILWIND_CLI_VERSION = "3.4.0"
TAILWIND_CLI_SRC_CSS = BASE_DIR / "myresume" / "assets-src" / "css" / "main.css"
TAILWIND_CLI_DIST_CSS = "css/main.css"
TAILWIND_CLI_PATH = BASE_DIR / "bin"

# Google Fonts
# https://github.com/andymckay/django-google-fonts

GOOGLE_FONTS = ["Ubuntu", "Press Start 2P"]

# Custom settings

DATA_DIR = BASE_DIR / "myresume" / "data"
DIST_DIR = BASE_DIR / "dist"

LANG: Literal["en", "fr"] = env.get("RESUME_LANG", "en")  # type: ignore
assert LANG in ("en", "fr")

# Used for links to HTML & PDF files in the top right links:
ROOT_PATH = env.get("ROOT_PATH", "/")
DEBUG_LAYOUT = bool(env.get("DEBUG_LAYOUT", ""))
