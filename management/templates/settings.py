# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

"""
settings.py -- Local site settings

Override in this what you wish.  By default it simply imports the
site default settings and overrides nothing.

This file should *not* be checked into git.
"""

from siteSettings import *  # pylint: disable=W0401

# Make this unique, and don't share it with anybody.  Used by Django's
# cookie-based authentication mechanism.
SECRET_KEY = '{{ secretKey }}'

# For example, override the database settings:
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'dev.db'
#    }
#}
