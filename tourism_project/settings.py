"""
Django settings for tourism_project project.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vi5wnnw9i!b#avi5+d=cesi%62$iv#_8$zdesx=p+jawfsf0tg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Added for admin interface
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'crispy_forms',
    'modeltranslation',
    'corsheaders',
    'django_filters',
    'django_ckeditor_5', # Replaced 'ckeditor' with 'django_ckeditor_5'
    'widget_tweaks',  # Add this line after other third-party apps
    

    # Project apps
    'core',
    'users',
    'tour',
    'booking',
    'blog',
    'reviews', # Re-added dedicated reviews app
    'payments',
    'chatbots',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For internationalization
    'corsheaders.middleware.CorsMiddleware',  # For CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Added allauth middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Added for Gzip compression
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

# Cache Middleware (Update must come before Fetch)
MIDDLEWARE.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')


ROOT_URLCONF = 'tourism_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # For internationalization
                'core.context_processors.currency_processor', # Added currency context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'tourism_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache configuration (using database cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# For production, consider using PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'tourism_db',
#         'USER': 'db_user',
#         'PASSWORD': 'db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Available languages
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')), # Corrected label for 'de'
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('ar', 'en', 'fr', 'de') # Uses German ('de')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add node_modules to static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# Django AllAuth Configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# AllAuth settings
SITE_ID = 1

# Updated AllAuth settings using new format
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'first_name*',
    'last_name*',
    'password1*',
    'password2*'
]
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Custom adapters
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

# Remove these deprecated settings:
# ACCOUNT_AUTHENTICATION_METHOD
# ACCOUNT_EMAIL_REQUIRED
# ACCOUNT_USERNAME_REQUIRED
# ACCOUNT_SIGNUP_FORM_CLASS

# Forms
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# Social account providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-secret',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-secret',
            'key': ''
        },
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
    }
}

LOGIN_REDIRECT_URL = 'core:home' # Use namespaced URL
LOGOUT_REDIRECT_URL = 'core:home' # Use namespaced URL

# Default Currency (used as base for exchange rates)
# Currency settings
DEFAULT_CURRENCY_CODE = 'USD'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# For production, use SMTP:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-password'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Payment gateway settings
STRIPE_PUBLIC_KEY = 'your-stripe-public-key'
STRIPE_SECRET_KEY = 'your-stripe-secret-key'
PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_SECRET = 'your-paypal-secret'

# Celery settings (for background tasks)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Chatbot settings
OPENAI_API_KEY = 'your-openai-api-key'  # For OpenAI integration
DIALOGFLOW_PROJECT_ID = 'your-dialogflow-project-id'  # For Dialogflow integration

# Consider replacing CKEditor with CKEditor 5
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
            ]
        }
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote',
        'imageUpload', '|', 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
        'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', 'imageTitle', '|', 'imageStyle:alignLeft', 'imageStyle:full',
                       'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells' ]
        },
        'height': 400,
        'width': '100%',
    }
}

# Add custom upload path for CKEditor 5
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_UPLOAD_PATH = 'uploads/ckeditor/'


# Production settings
if not DEBUG:
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    
    # Security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    X_FRAME_OPTIONS = 'DENY'
    
    # Add whitenoise for static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
