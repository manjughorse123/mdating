"""
Django settings for DatingApp project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import datetime
import os.path
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8(y+s39b-%2r0gi(tzp-m!a&wl21r#xgt#75mt#s_d)y38wqyo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '0.0.0.0', '0.0.0.0:81']
# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    # 'admin_interface',
    'django_toggle_switch_widget',
    'django_object_actions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'ckeditor',
    'main',
    'account',
    'django.contrib.gis',
    'post',
    'usermedia',
    'friend',
    'matchprofile',
    'django_filters',

    'rest_framework_gis',
    'rest_framework_json_api',
    'likeuser',
    'colorfield',
    'masterdata',
    'chatbot',
    "fcm_django",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DatingApp.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'DatingApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'DatingApps',
#        'USER': 'postgres',
#        'PASSWORD': 'toor',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
# }

# DATABASES = {
#     'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dating',
#         'USER': 'datinguser',
#         'PASSWORD': 'dating',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mydate',
        'USER': 'django',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# GDAL_LIBRARY_PATH = "/opt/homebrew/Cellar/gdal/3.3.2_3/lib/libgdal.dylib" 
# GEOS_LIBRARY_PATH = "/opt/homebrew/Cellar/geos/3.9.1/lib/libgeos_c.dylib"



# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.sqlite3',
#         'ENGINE': 'django.contrib.gis.db.backends.spatialite',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    "site_title": " Dating Apps",
    "site_header": "Dating Apps",
    "site_brand": "ByteCipher",
    "changeform_format": "single"
}

# Sms gateway Authentication Keys
AUTH_KEY = 'YOUR_KEY_HERE'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    '   DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework.filters.DjangoFilterBackend',
        #                             'rest_framework.filters.OrderingFilter',

    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),



    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',  # THIS ONE
    #     'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    #     'drf_social_oauth2.authentication.SocialAuthentication',
    # ),


}

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES':
#         ('rest_framework.permissions.IsAuthenticated',),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         #   'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#             'rest_framework.authentication.SessionAuthentication',
#             'rest_framework.authentication.BasicAuthentication',),
# }
# AUTH_USER_MODEL = 'account.User'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'JSON_EDITOR': True,
    'DEFAULT_MODEL_DEPTH': -1
}


AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

#   'DEFAULT_PARSER_CLASSES': (
#           'rest_framework.parsers.FormParser',
#           'rest_framework.parsers.MultiPartParser',
#           'rest_framework.parsers.JSONParser',
#    )
# JWT_AUTH = {
#     # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'account.utils.my_jwt_response_handler',
#     # 'JWT_ENCODE_HANDLER':
#     # 'rest_framework_jwt.utils.jwt_encode_handler',
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'account.utils.jwt_response_payload_handler',
#     'JWT_PAYLOAD_HANDLER': 'account.utils.jwt_payload_handler',
#     'JWT_VERIFY': True,
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
# }


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'account.authentication.SafeJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # make all endpoints private
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': [],
    # 'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}


REFRESH_TOKEN_SECRET = 'django-insecure-8(y+s39b-%2r0gi(tzp-m!a&wl21r#xgt#75mt#s_d)y38wqyo'

DEFAULTS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
}

import firebase_admin
from firebase_admin import credentials

data = os.path.join(BASE_DIR, 'firebasedata') + "/serviceAccountKey.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)