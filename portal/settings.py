"""
Settings base de Django para JobLink Portal.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# CONFIGURACIÓN GENERAL
# ===========================

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'reemplazar-esta-clave-en-produccion')

# En producción, Render NO define DJANGO_DEBUG, así que esto queda en False
DEBUG = True

# Hosts permitidos (Render + Firebase)
ALLOWED_HOSTS = [
    'joblink-tkm2.onrender.com',
    'arcadea.web.app',
    'localhost',
    '127.0.0.1'
]

# ===========================
# APLICACIONES
# ===========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ✅ Corrección importante
    'portal.core',
]

# ===========================
# MIDDLEWARE
# ===========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portal.urls'

# ===========================
# TEMPLATES
# ===========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'portal' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'

# ===========================
# BASE DE DATOS
# ===========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================
# VALIDADORES
# ===========================

AUTH_PASSWORD_VALIDATORS = []

# ===========================
# LOCALIZACIÓN
# ===========================

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ===========================
# ARCHIVOS ESTÁTICOS
# ===========================

STATIC_URL = '/static/'

# Para producción (Render)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Para desarrollo (si tienes carpeta static/)
STATICFILES_DIRS = [
    BASE_DIR / 'portal' / 'static'
]

# ===========================
# CONFIG API NODE.JS
# ===========================

API_BASE = os.getenv('API_BASE', "http://localhost:8080")
API_TOKEN = os.getenv('API_TOKEN', "secreto123")
ADMIN_EMAILS = os.getenv('ADMIN_EMAILS', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

