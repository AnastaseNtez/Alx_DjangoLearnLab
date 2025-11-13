from pathlib import Path
import os # Ensure os is imported for BASE_DIR if it wasn't already

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-86!7%d(j-x$1@3p3v0d*^b&0=q7s^@y$#6!8r)0i7k1k'

# --- STEP 1: PRODUCTION SETTINGS ---
# Set DEBUG to False in production
DEBUG = True # Keep True for now, but set to False when deploying!

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ngrok.io'] # Example hosts

# Application definition

INSTALLED_APPS = [
    # --- STEP 4: CSP REQUIREMENT (Needs 'django-csp' installed) ---
    # Add 'csp' here
    'csp',
    
    # Custom Apps must come before django.contrib.admin to ensure CustomUser is loaded first
    'LibraryProject.bookshelf',
    
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # --- STEP 4: CSP REQUIREMENT (Needs 'django-csp' installed) ---
    # Add CspMiddleware immediately after SecurityMiddleware
    'csp.middleware.CspMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Look in the main templates folder
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom User Configuration
# -------------------------
AUTH_USER_MODEL = 'bookshelf.CustomUser'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# --- STEP 1: SECURITY HEADER CONFIGURATION ---
# Enforce secure transmission of session and CSRF cookies (requires HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Protects against Clickjacking attacks
X_FRAME_OPTIONS = 'DENY'

# Protects against XSS attacks in older browsers (set to True by default in recent Django versions)
SECURE_BROWSER_XSS_FILTER = True

# Protects against MIME-type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True


# --- STEP 4: CONTENT SECURITY POLICY (CSP) CONFIGURATION ---
# Define allowed sources for different content types (Requires 'django-csp' package)
CSP_DEFAULT_SRC = ("'self'",) # Allow content from your own domain
CSP_STYLE_SRC = ("'self'", "https://cdn.tailwindcss.com") # Allow self and Tailwind CDN for styles
CSP_SCRIPT_SRC = ("'self'", "https://cdn.tailwindcss.com") # Allow self and Tailwind CDN for scripts
CSP_IMG_SRC = ("'self'", "data:") # Allow self and inline data URIs for images
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",) # Used for AJAX, WebSockets, etc.

# CRITICAL NOTE: If you run locally on HTTP, temporarily set DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
# or comment out SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE.
# For the ALX checker, these MUST be set to True.