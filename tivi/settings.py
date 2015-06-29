# Django settings for tivi project.
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)
STATIC_URL =os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS =('static-assets',)
DEBUG = False #Set to True when only developing the system, not good for celery
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}"""

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost"]




# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
"""STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)"""


#STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_-9(_et=+1xyp8behr_ycbf+54x(6)t$rjwa0es*l4=oulq0i4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tivi.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tivi.wsgi.application'

"""TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)"""

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tiviapp',
    'mongoengine.django.mongo_auth',
    'djgeojson',
    'geocoder',
    'datetimewidget',
    'django_shell_ipynb',
    'django_extensions',
    'jquery',
    'bootstrap3',
    'rest_framework_mongoengine',
    'rest_framework',
    'django_tables2',
    'emoticons',
    'debug_toolbar',
    "djcelery",
    'tastypie',
    'chartit',
    'splearn',

)
#import mongoengine.django.mongo_auth.models
#App to add django-fbauth-templatetag,twitter-text-py,
##Added in this project
#AUTHENTICATION_BACKENDS = ('neo4django.graph_auth.backends.NodeModelBackend',)
#AUTH_USER_MODEL = 'graph_auth.User'
AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
#LOGIN_URL = 'login'
#LOGIN_REDIRECT_URL = 'main'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
SERIALIZATION_MODULES = {
    'geojson' : 'djgeojson.serializers'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
from mongoengine import connect

connect(db="mediapower", username="media", password="media");
NEO4J_DATABASES = {
    'default' : {
        'HOST':'localhost',
        'PORT':7474,
        'ENDPOINT':'/db/data',
        #'OPTIONS': {'username': 'neo4j',
        #'password': 'socialapp'}
    }
}
DATABASE_ROUTERS = ['neo4django.utils.Neo4djangoIntegrationRouter']


NEO4DJANGO_PROFILE_REQUESTS = False
NEO4DJANGO_DEBUG_GREMLIN = False
import djcelery
djcelery.setup_loader()
#BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True

import sys
# Path for spark source folder
os.environ['SPARK_HOME']="/opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/lib/spark"
os.environ['JAVA_HOME']="/usr/jdk64/jdk1.7.0_67/jre/"
#os.environ['PYSPARK_SUBMIT_ARGS']="--master yarn-client --driver-memory 512m --executor-memory 512m --num-executors 2"


# Append pyspark  to Python Path
sys.path.append("/opt/cloudera/parcels/CDH-5.3.0-1.cdh5.3.0.p0.30/lib/spark/python")
"""
try:
    from pyspark import SparkContext,SparkConf
    from pyspark.streaming import StreamingContext
    print ("Successfully imported Spark Modules")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)"""


######

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
