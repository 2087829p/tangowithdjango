"""
Django settings for tango_with_django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0n$4*%8ln15q1o22v%an=qh6@&ik0ba+iq$jdw%ajwixwi8hx9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin', # THIS LINE SHOULD NOW BE UNCOMMENTED
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'rango',
	'registration',
)

SITE_ID = 1
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_with_django_project.urls'
WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'
SESSION_EXPIRE_AT_BROWSER_CLOSE=True


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     TEMPLATE_PATH,
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASE_PATH = os.path.join(PROJECT_PATH, 'rango.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_PATH = os.path.join(PROJECT_PATH,'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    STATIC_PATH,
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') 

REGISTRATION_OPEN = True                # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = '/rango/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,

