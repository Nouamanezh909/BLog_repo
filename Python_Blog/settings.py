"""
Django settings for Python_Blog project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import os.path
# Importing django heroku here
import django_heroku 

#importing new modules to defrnciate between heroku and django databases 
import dj_database_url
# problem loading this with pip 
import dotenv

# understanding project root and base dir 
#BASE_DIR is where your manage.py lies, and PROJECT_ROOT is BASE_DIR + your_project_name (where settings.py is).

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Adding the will force the app to use (SQL) database locally but not with heroku 
dotenv_file  = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# UPdating template paths so can heroku load the template's site 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "2xvexz-0c3-b@nni%g&mwdpqoqe_tyz=^c10v)i#ntr8scrvoe"


# Updating security key to use mine
SECRET_KEY = os.environ.get('Secret_Key')

# SECURITY WARNING: don't run with debug turned on in production!
# Turning debug into condition boolean when going Live


# etting Debug value to False whene going Live 
DEBUG = False 

# Allowing hosts for assccessing the site 
ALLOWED_HOSTS = ['bloggingtopics.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",  
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party app here
    "crispy_forms",
    # New installed app here
    # Posts app
    'Posts.apps.PostsConfig',
    # Accounts app
    'Accounts.apps.AccountsConfig',
]

# Telling django to use my new custom user model
AUTH_USER_MODEL = 'Accounts.User'

# Using the Bootstrap 4 instead of built in version 2 or 3
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
        # Serving static fies with whitenoise module 
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

#Adding the  compress 
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

ROOT_URLCONF = "Python_Blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # mapping my templates to heroku 
            os.path.join(BASE_DIR, 'Posts/Templates') , 
            os.path.join(BASE_DIR, 'Accounts/Templates')
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "Python_Blog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases



# changing the database to respond wethere the app called locally or remotlly 
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# New Entry 
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'

# Deployment
STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")

# When run collectstatic static dirs will point to the correct s.file
STATICFILES_DIRS =(
    os.path.join(PROJECT_ROOT, 'static'),
)

# Addinding the static files storage / Simplify the serving proccess !
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Config
MEDIA_URL = '/media/'   

# Deployemnt
MEDIA_ROOT = os.path.join(BASE_DIR, "live-static", "media-root")


# Setting a Logout redirect url
LOGOUT_REDIRECT_URL = '/Login'
LOGIN_REDIRECT_URL = '/Index'

# this line will take care of changing the settings automaticlly
django_heroku.settings(locals())

# Making heroku postgresql forget about using SSl mode 
del DATABASES['default'] ['OPTIONS'] ['sslmode']


# PAssing new info to solve 500 erro 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}