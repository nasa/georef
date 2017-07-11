#!/usr/bin/env python
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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "georef.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
