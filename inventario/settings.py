# inventario/settings.py
from pathlib import Path
import os

# Base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad (en producción usa variables de entorno)
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure--qs%g)rnhs3=diwpcgysi7tr_t^t(+0!)_lkke!fwa6a3jg1qo"  # solo para local
)

# DEBUG: por defecto True en local. En la nube pon DJANGO_DEBUG=0
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

# ALLOWED_HOSTS: en la nube define ALLOWED_HOSTS="tu-dominio.com,otro.com"
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h] if not DEBUG else []

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "inventario_app",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <- para servir estáticos en la nube
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

# ===========================
# Base de datos
# ===========================
# En tu PC sigue MSSQL (como ya lo tenías).
# En la nube, si pones USE_SQLITE=1, cambia automáticamente a SQLite (más simple y gratis).
if os.getenv("USE_SQLITE") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "NAME": "inventario_db",
            "HOST": r"(localdb)\MSSQLLocalDB",
            "OPTIONS": {
                "driver": "ODBC Driver 17 for SQL Server",
                "trusted_connection": "yes",
            },
        },
    }

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalización
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "static/"
# Donde collectstatic guardará todo para producción
STATIC_ROOT = BASE_DIR / "staticfiles"

# En producción (DJANGO_PROD=1) usa almacenamiento comprimido con manifest
if os.getenv("DJANGO_PROD") == "1":
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# ===========================
# API de Contabilidad
# ===========================
CONTABILIDAD_API_URL = "http://3.80.223.142:3001/api/public/entradas-contables"
# En producción define CONTABILIDAD_API_KEY como variable de entorno
CONTABILIDAD_API_KEY = os.getenv(
    "CONTABILIDAD_API_KEY",
    "ak_live_d16e8b7e2481092b3c26a7578eeeae747db15b5ab57b9f5b"  # solo para local
)
