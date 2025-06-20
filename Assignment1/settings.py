from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g0xokdiq@v8hxcp4(d%)_lk*8_+akaet6_tspwtybay-9=$720'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservations.apps.ReservationsConfig',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Assignment1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # for global templates like registration/login.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Assignment1.wsgi.app'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


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

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ LOGIN + REDIRECTS
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'  # send the user to home after login
LOGOUT_REDIRECT_URL = 'home'  # optional: after logout






# ✅ EMAIL BACKEND for SendGrid (Secure & Production-Ready)
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

# ✅ Load SendGrid key from environment variable
import os
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Optional Settings

SENDGRID_ECHO_TO_STDOUT = True
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
DEFAULT_FROM_EMAIL = "mannatsareen1998@gmail.com"




CORS_ALLOW_ALL_ORIGINS = True  # for development only

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
