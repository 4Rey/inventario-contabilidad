# inventario/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Core =====
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure--qs%g)rnhs3=diwpcgysi7tr_t^t(+0!)_lkke!fwa6a3jg1qo')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Local por defecto; en Render se sobreescribe (ver más abajo)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'inventario_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise para servir estáticos en la nube
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'inventario.wsgi.application'

# ===== DB: local SQL Server, nube SQLite =====
if os.getenv('RENDER'):     # Render seteará RENDER=1
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'inventario_db',
            'HOST': r'(localdb)\MSSQLLocalDB',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': 'yes',
            },
        },
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

# ===== Static =====
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# ===== API Contabilidad =====
CONTABILIDAD_API_URL = 'http://3.80.223.142:3001/api/public/entradas-contables'
# En la nube lo leeremos del env var; local usamos tu key por defecto
CONTABILIDAD_API_KEY = os.getenv(
    'CONTABILIDAD_API_KEY',
    'ak_live_d16e8b7e2481092b3c26a7578eeeae747db15b5ab57b9f5b'
)

# Si estamos en Render, ajustamos hosts permitidos
if os.getenv('RENDER'):
    ALLOWED_HOSTS = ['.onrender.com']
