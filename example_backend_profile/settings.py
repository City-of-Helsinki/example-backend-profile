from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, ""),
    ALLOWED_HOSTS=(list, []),
    OIDC_AUDIENCE=(str, ""),
    OIDC_API_SCOPE_PREFIX=(str, ""),
    OIDC_API_AUTHORIZATION_FIELD=(str, ""),
    OIDC_REQUIRE_API_SCOPE_FOR_AUTHENTICATION=(bool, False),
    OIDC_ISSUER=(str, ""),
    SOCIAL_AUTH_TUNNISTAMO_KEY=(str, ""),
    SOCIAL_AUTH_TUNNISTAMO_SECRET=(str, ""),
    SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT=(str, ""),
    GDPR_API_QUERY_SCOPE=(str, ""),
    GDPR_API_DELETE_SCOPE=(str, ""),
    HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED=(bool, False),
    HELSINKI_PROFILE_API_URL=(str, ""),
)

environ.Env.read_env(str(BASE_DIR / "config.env"))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "XXX"


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "helusers.apps.HelusersConfig",
    "helusers.apps.HelusersAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "social_django",
    "users",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example_backend_profile.urls"

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

WSGI_APPLICATION = "example_backend_profile.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Authentication

AUTHENTICATION_BACKENDS = (
    "helusers.tunnistamo_oidc.TunnistamoOIDCAuth",
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/admin/"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("helusers.oidc.ApiTokenAuthentication",),
}

OIDC_API_TOKEN_AUTH = {
    "AUDIENCE": env("OIDC_AUDIENCE"),
    "API_SCOPE_PREFIX": env("OIDC_API_SCOPE_PREFIX"),
    "API_AUTHORIZATION_FIELD": env("OIDC_API_AUTHORIZATION_FIELD"),
    "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": env(
        "OIDC_REQUIRE_API_SCOPE_FOR_AUTHENTICATION"
    ),
    "ISSUER": env("OIDC_ISSUER"),
}

SOCIAL_AUTH_TUNNISTAMO_KEY = env("SOCIAL_AUTH_TUNNISTAMO_KEY")
SOCIAL_AUTH_TUNNISTAMO_SECRET = env("SOCIAL_AUTH_TUNNISTAMO_SECRET")
SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT = env("SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT")

from helusers.defaults import SOCIAL_AUTH_PIPELINE

HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED = env("HELUSERS_BACK_CHANNEL_LOGOUT_ENABLED")


# Helsinki GDPR API

GDPR_API_URL_PATTERN = "v1/user/<uuid:uuid>"
GDPR_API_MODEL = "users.UserData"
GDPR_API_MODEL_LOOKUP = "user__uuid"
GDPR_API_QUERY_SCOPE = env("GDPR_API_QUERY_SCOPE")
GDPR_API_DELETE_SCOPE = env("GDPR_API_DELETE_SCOPE")
GDPR_API_DELETER = "users.gdpr.delete_gdpr_data"


# Helsinki profile API

HELSINKI_PROFILE_API_URL = env("HELSINKI_PROFILE_API_URL")


# Password validation

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


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Cross-Origin Resource sharing

CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r"^/api/v1/(?:myuserdata|fillmybirthday)/$"
