# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import sys
import tempfile
import re


def getEnvironmentFromSourceMe(d='.'):
    # pick up environment variables from sourceme
    fd, varsFile = tempfile.mkstemp('djangoWsgiSourceMe.txt')
    os.close(fd)

    ret = os.system('bash -c "(source %s/sourceme.sh && printenv > %s)"' % (d, varsFile))
    if ret != 0:
        varsFile = '%s/vars.txt' % d
        print >> sys.stderr, 'djangoWsgi.py: could not auto-generate environment from sourceme.sh, trying to fall back to manually generated file %s' % varsFile
        # fallback: user can manually generate vars.txt file by sourcing sourceme.sh and running 'printenv > vars.txt'

    varsIn = file(varsFile, 'r')
    for line in varsIn:
        line = line[:-1]  # chop final cr
        if '=' not in line or '=()' in line:
            continue
        var, val = line.split('=', 1)
        os.environ[var] = val
    varsIn.close()
    try:
        os.unlink(varsFile)
    except OSError:
        pass

    # set up virtualenv if needed
    if 'VIRTUAL_ENV' in os.environ:
        activateFile = '%s/bin/activate_this.py' % os.environ['VIRTUAL_ENV']
        execfile(activateFile, {'__file__': activateFile})

    # add any new entries from PYTHONPATH to Python's sys.path
    if 'PYTHONPATH' in os.environ:
        envPath = re.sub(':$', '', os.environ['PYTHONPATH'])
        sys.path = envPath.split(':') + sys.path


def sendError(start_response, text):
    start_response(text, [('Content-type', 'text/html')])
    return ["""<html>
  <head><title>%s</title></head>
  <body><h1>%s</h1></body>
</html>
    """ % (text, text)]


def downForMaintenance(environ, start_response):
    import stat
    import time
    d = os.path.dirname(os.path.realpath(__file__))
    downFile = os.path.join(d, 'DOWN_FOR_MAINTENANCE')
    downMtime = os.stat(downFile)[stat.ST_MTIME]
    downTimeString = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(downMtime))
    return sendError(start_response, '503 Down for maintenance since %s' % downTimeString)

thisDir = os.path.dirname(os.path.realpath(__file__))
getEnvironmentFromSourceMe(thisDir)
if os.path.exists(os.path.join(thisDir, 'DOWN_FOR_MAINTENANCE')):
    application = downForMaintenance
else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()