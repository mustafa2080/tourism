"""
Railway-specific settings for production deployment
"""
import os
from tourism_project.settings import *

# Force production mode
DEBUG = False

# Railway-specific environment variables
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT', 'production')

# Allowed hosts for Railway
ALLOWED_HOSTS = [
    '.railway.app',
    '.up.railway.app',
    'localhost',
    '127.0.0.1'
]

# Add Railway public domain if available
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN'))

# Add custom domain if provided
if 'ALLOWED_HOSTS' in os.environ:
    custom_hosts = os.environ.get('ALLOWED_HOSTS', '').split(',')
    ALLOWED_HOSTS.extend([host.strip() for host in custom_hosts if host.strip()])

# CSRF Trusted Origins for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app'
]

# Add Railway public domain to CSRF trusted origins
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{domain}',
        f'http://{domain}'  # For development/testing
    ])

# Security settings for Railway
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CSRF settings optimized for Railway
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# Database configuration
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
    print(f"Using database: {DATABASES['default']['ENGINE']}")
else:
    print("No DATABASE_URL found, using SQLite")

# Static files for Railway
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email configuration for Railway
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# PayPal settings for Railway
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', '')
PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET', '')

# Site URL for Railway
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    SITE_URL = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}"
    SITE_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
else:
    SITE_URL = 'https://your-app.railway.app'
    SITE_DOMAIN = 'your-app.railway.app'

# Update PayPal URLs with correct site URL
PAYPAL_RETURN_URL = f"{SITE_URL}/en/payments/confirm/"
PAYPAL_CANCEL_URL = f"{SITE_URL}/en/payments/cancel/"

print(f"Railway settings loaded:")
print(f"- DEBUG: {DEBUG}")
print(f"- ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"- CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
print(f"- SITE_URL: {SITE_URL}")
