#!/usr/bin/env python
import time
import datetime
import subprocess
import os.path
from os import listdir

import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
from georef_imageregistration import offline_config, output_generator, registration_common


#  If center point available, autoregister and write output to db,
#    elif geosens available, autoregister  and write output to db,
#    elif nadir available, autoregister  and write output to db,


def autoregisterAndOutput():
    pass

autoregisterAndOutput()