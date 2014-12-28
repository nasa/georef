#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import sys

# try to bootstrap before hooking into django management stuff
if 'bootstrap' in sys.argv:
    extraArgs = sys.argv[2:]
else:
    extraArgs = []
ret = os.spawnl(os.P_WAIT, sys.executable, sys.executable,
                '%s/management/bootstrap.py' % os.path.dirname(__file__),
                *extraArgs)
if ret != 0 or extraArgs:
    sys.exit(ret)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geoRef.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
