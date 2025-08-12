# inventario/settings.py
from pathlib import Path
import os
from urllib.parse import urlparse
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Seguridad / Debug
# -------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure--qs%g)rnhs3=diwpcgysi7tr_t^t(+0!)_lkke!fwa6a3jg1qo"
)
DEBUG = os.getenv("DEBUG", "0") == "1"

# Hosts (local + Render)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
if RENDER_EXTERNAL_URL:
    _u = urlparse(RENDER_EXTERNAL_URL)
    if _u.hostname:
        ALLOWED_HOSTS.append(_u.hostname)

# CSRF en Render (Django 5 exige origenes)
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]
if RENDER_EXTERNAL_URL:
    _u = urlparse(RENDER_EXTERNAL_URL)
    CSRF_TRUSTED_ORIGINS.append(f"{_u.scheme}://{_u.hostname}")

# Detrás de proxy HTTPS (Render)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------
# Apps
# -------------------------------
INSTALLED_APPS = [
    # Para que whitenoise tome control en runserver
    "whitenoise.runserver_nostatic",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "inventario_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para archivos estáticos
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "inventario.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "inventario.wsgi.application"

# -------------------------------
# Base de datos
# -------------------------------
# En Render/Neon usamos DATABASE_URL; localmente cae a SQLite.
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,   # pooling
            ssl_require=True,   # Neon usa SSL
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------
# Password validation
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------
# Internacionalización
# -------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------
# Archivos estáticos
# -------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise: archivos comprimidos y con manifest
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------
# Primary key por defecto
# -------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# -------------------------------
# API de Contabilidad 
# -------------------------------
CONTABILIDAD_API_URL = "http://3.80.223.142:3001/api/public/entradas-contables"
CONTABILIDAD_API_KEY = "ak_live_d16e8b7e2481092b3c26a7578eeeae747db15b5ab57b9f5b"
