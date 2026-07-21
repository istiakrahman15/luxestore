"""
Django settings for the LuxeStore project.

LuxeStore is a portfolio demo storefront. It intentionally has no
authentication, cart, checkout, or payment logic — see the README for scope.

Environment-aware by design:
- Locally, with no environment variables set, it just works with SQLite and
  DEBUG on.
- On Vercel (or any host that provides a DATABASE_URL / SECRET_KEY / etc via
  env vars), it automatically switches to Postgres and a hardened config.
  See README.md -> "Deploying to Vercel" for the full walkthrough.
"""

import os
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Loads variables from a local .env.local file (created by `vercel pull`,
# or written by hand for local testing) if python-dotenv is installed and
# the file exists. Safe to leave in place everywhere — it's a no-op if
# there's no .env.local. Never commit .env.local to version control.
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env.local")
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Core / security settings
# ---------------------------------------------------------------------------

# SECURITY WARNING: this fallback key is fine for local development only.
# In production (Vercel or elsewhere), set a real SECRET_KEY environment
# variable — never rely on this default outside your own machine.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-luxestore-demo-key-change-before-deploy-9f2k4m",
)

# DEBUG defaults to True locally. On Vercel, set the env var DEBUG=False.
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Comma-separated list of allowed hosts, e.g. "myapp.vercel.app,example.com".
# Defaults cover local development out of the box.
_allowed_hosts_env = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_env.split(",") if h.strip()] or [
    "127.0.0.1",
    "localhost",
]
# Always allow Vercel's own preview/production domains without extra config.
ALLOWED_HOSTS.append(".vercel.app")

# Required by Django's CSRF protection when served over HTTPS behind Vercel.
_csrf_origins_env = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins_env.split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'store.apps.StoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Serves static files efficiently without a separate web server —
    # active for local `runserver` / `vercel dev`. On real Vercel
    # deployments, static files are served straight from the CDN instead,
    # so this middleware simply isn't exercised there.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luxestore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Makes the store name / tagline available in every template
                'store.context_processors.site_meta',
            ],
        },
    },
]

WSGI_APPLICATION = 'luxestore.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# Locally: SQLite, zero configuration needed.
# On Vercel (or any host that sets DATABASE_URL, e.g. a Postgres add-on):
# automatically switches to Postgres. Install psycopg2-binary (already in
# requirements.txt) for this to work.
_database_url = os.environ.get("DATABASE_URL")

if _database_url:
    _parsed = urllib.parse.urlparse(_database_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _parsed.path.lstrip("/"),
            "USER": _parsed.username,
            "PASSWORD": _parsed.password,
            "HOST": _parsed.hostname,
            "PORT": _parsed.port,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (product images uploaded via the admin).
# NOTE: Vercel's filesystem is ephemeral/read-only at runtime, so anything
# uploaded here will NOT persist between deployments or across requests in
# production. Locally this works normally. For persistent uploads on
# Vercel, wire up django-storages with an S3-compatible bucket (e.g.
# Cloudflare R2) — see README.md for pointers. Until then, products without
# an image simply show their built-in placeholder tile, which is the
# expected/default look for this demo.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise: serve static files straight from the app's static/ directories
# when DEBUG is on (no collectstatic needed locally), and from STATIC_ROOT
# once collectstatic has run in production.
WHITENOISE_USE_FINDERS = DEBUG

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Security hardening (only meaningfully active when DEBUG=False)
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
