"""Settings da Livraria Awesome — tudo lido do .env com django-environ."""
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# --- django-environ -------------------------------------------------------
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])
DATABASES = {"default": env.db("DATABASE_URL")}
# --------------------------------------------------------------------------

# Liga/desliga o tema django-unfold (USE_UNFOLD=False = admin padrão do Django)
USE_UNFOLD = env.bool("USE_UNFOLD", default=True)

UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.simple_history",
]

INSTALLED_APPS = (UNFOLD_APPS if USE_UNFOLD else []) + [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # terceiros
    "corsheaders",
    "rest_framework",
    "django_filters",
    "storages",
    "simple_history",
    "import_export",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "silk",
    # projeto
    "loja",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

SITE_ID = 1

# --- arquivos estáticos (whitenoise) e mídia (django-storages) -------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default=None)
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default=None)
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="livraria")
AWS_S3_REGION_NAME = "us-east-1"
AWS_QUERYSTRING_EXPIRE = 3600  # URL assinada vale 1 hora

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage"
        if AWS_S3_ENDPOINT_URL
        else "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- django-cors-headers ----------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# --- Django REST framework + django-filter ---------------------------------
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# --- django-allauth ---------------------------------------------------------
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = "/"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"]},
    "github": {"SCOPE": ["user:email"]},
}

# --- django-silk ------------------------------------------------------------
SILKY_PYTHON_PROFILER = False
SILKY_META = True

# --- django-unfold ----------------------------------------------------------
UNFOLD = {
    "SITE_TITLE": "Livraria Awesome",
    "SITE_HEADER": "Livraria Awesome",
    "SITE_SYMBOL": "menu_book",
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "oklch(97.7% .014 308.299)",
            "100": "oklch(94.6% .033 307.174)",
            "200": "oklch(90.2% .063 306.703)",
            "300": "oklch(82.7% .119 306.383)",
            "400": "oklch(71.4% .203 305.504)",
            "500": "oklch(62.7% .265 303.9)",
            "600": "oklch(55.8% .288 302.321)",
            "700": "oklch(49.6% .265 301.924)",
            "800": "oklch(43.8% .218 303.724)",
            "900": "oklch(38.1% .176 304.987)",
            "950": "oklch(29.1% .149 302.717)",
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
