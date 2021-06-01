#__BEGIN_LICENSE__
# Copyright (c) 2017, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The GeoRef platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

# siteSettings.py -- site default settings
#
# This contains the default settings for the site-level django app.  This will
# override any application-default settings and define the default set of
# installed applications. This should be a full settings.py file which needs
# minimal overrides by the settings.py file for the application to actually
# function.
#
# As a bare minimum, please edit INSTALLED_APPS!
#
# This file *should* be checked into git.
import sys
import os
import importlib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf.global_settings import ALLOWED_HOSTS

# apps should be listed from "most specific" to "most general".  that
# way, templates in more specific apps override ones from more general
# apps.
INSTALLED_APPS = ['georefApp',
                  'geocamTiePoint',
                  'geocamUtil',
                  'georef_imageregistration',
                  'geocamPycroraptor2',

                  'deepzoom',
                  'django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  ]

for app in INSTALLED_APPS:
    try:
        appSettings = importlib.import_module(app + ".defaultSettings")
        for key, val in vars(appSettings).iteritems():
            if not key.startswith('_'):
                globals()[key] = val
    except:
        pass

USING_DJANGO_DEV_SERVER = ('runserver' in sys.argv)
USING_APP_ENGINE = False
USE_STATIC_SERVE = USING_DJANGO_DEV_SERVER

SCRIPT_NAME = os.environ['DJANGO_SCRIPT_NAME']  # set in sourceme.sh
if USING_DJANGO_DEV_SERVER:
    # django dev server deployment won't work with other SCRIPT_NAME settings
    SCRIPT_NAME = '/'


DEBUG = True
# TO TEST DEBUG FALSE YOUR IP FOR VM MUST BE LISTED BELOW
# TODO include real url hostname for staging and production; override production's in settings.py
#ALLOWED_HOSTS = ['10.0.3.22', 
#                 '10.0.3.18']

# TEMPLATE_DEBUG = DEBUG

    
PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
if not PROJ_ROOT.endswith('/'):
    PROJ_ROOT += '/'

# Python path is agnostic to what the site-level dir is. It also prefers the
# checked-out version of an app over the standard python install locations.
sys.path.append(PROJ_ROOT)

ADMINS = (
    # ('NASA Intelligent Robotics Group', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql', # django.db.backends.mysql',
        'NAME': 'georef',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# for auto image registration. set these in settings.py
GEOREF_DB_HOST="localhost"
GEOREF_DB_USER="root"
GEOREF_DB_PASS="vagrant"
GEOREF_DB_NAME="georef"

# Path to the input database
DB_PATH = '/home/username/db.sqlt'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds static.
# Example: "/home/static/static.lawrence.com/"
STATIC_ROOT = os.path.join(PROJ_ROOT, "build", "static")

# URL that handles the static served from STATIC_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://static.lawrence.com", "http://example.com/static/"
STATIC_URL = SCRIPT_NAME + 'static/'
EXTERNAL_URL = STATIC_URL

# Absolute path to the directory that holds data. This is different than static
# in that it's uploaded/processed data that's not needed for the operation of
# the site, but may need to be network-accessible, or be linked to from the
# database. Examples: images, generate kml files, etc.
# Example: "/data"
DATA_ROOT = os.path.join(PROJ_ROOT, 'data', '')

# URL that handles the data served from DATA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://data.lawrence.com", "http://example.com/data/"
DATA_URL = SCRIPT_NAME + 'data/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = DATA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = DATA_URL

# directory that holds the deepzoom tiles. 
DEEPZOOM_ROOT = DATA_ROOT + 'deepzoom/'
DEEPZOOM_URL = DATA_URL + 'deepzoom/'
DEFAULT_CREATE_DEEPZOOM_OPTION = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJ_ROOT, 'apps/georefApp/templates'),
            os.path.join(PROJ_ROOT, 'apps/geocamTiePoint/templates/'),

            # Templates for utility scripts
            os.path.join(PROJ_ROOT, 'bin/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'geocamUtil.context_processors.settings',
                'geocamUtil.context_processors.AuthUrlsContextProcessor.AuthUrlsContextProcessor',
                'geocamUtil.context_processors.SettingsContextProcessor.SettingsContextProcessor'
            ],
        },
    },
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Session Serializer: we use Pickle for backward compatibility and to allow more flexible session storage, but
# be sure to keep the SECRET_KEY secret for security (see:
# https://docs.djangoproject.com/en/1.7/topics/http/sessions/#session-serialization)
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'



MIDDLEWARE_CLASSES = (
    'geocamUtil.middleware.LogErrorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'geocamUtil.middleware.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

LOGIN_URL = SCRIPT_NAME + 'accounts/login/'
LOGIN_REDIRECT_URL = '/'

GEOCAM_UTIL_INSTALLER_USE_SYMLINKS = True
GEOCAM_UTIL_SECURITY_ENABLED = not USING_DJANGO_DEV_SERVER
GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT = False
GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS = False

GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT = 'write'

DEBUG_TOOLBAR = False
if DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1', '::1')  # TODO add your virtual machine's IP here
    DEBUG_TOOLBAR_PANELS = ['debug_toolbar.panels.versions.VersionsPanel',
                            'debug_toolbar.panels.timer.TimerPanel',
                            'debug_toolbar.panels.settings.SettingsPanel',
                            'debug_toolbar.panels.headers.HeadersPanel',
                            'debug_toolbar.panels.request.RequestPanel',
                            'debug_toolbar.panels.sql.SQLPanel',
                            'debug_toolbar.panels.staticfiles.StaticFilesPanel',
                            'debug_toolbar.panels.templates.TemplatesPanel',
                            'debug_toolbar.panels.cache.CachePanel',
                            'debug_toolbar.panels.signals.SignalsPanel',
                            'debug_toolbar.panels.logging.LoggingPanel',
                            'debug_toolbar.panels.redirects.RedirectsPanel',
                            ]
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,
                            }

VAR_ROOT = PROJ_ROOT + 'var/'

PYRAPTORD_SERVICE = False

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 604800,
    }
}


#===django-deepzoom settings====================================================
#  This logging profile should be added to your project settings to catch any 
#  file handling exceptions.
import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(DEEPZOOM_ROOT, 'deepzoom.exception.log'),
        },
    },
    'loggers': {
        'deepzoom.models': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


#EOF django-deepzoom test project settings
