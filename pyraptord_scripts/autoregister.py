#!/usr/bin/env python
import django
from django.conf import settings
django.setup()

from georef_imageregistration import registration_processor
from geocamUtil.imageInfo import dotdict


def autoregister():
    """
    Runs the registration_processor in georef_imageregistration app.
    """
    options = dotdict({'overwriteLevel': None, 
                       'numThreads': 4, 
                       'localSearch': False, 
                       'mission': None, 
                       'roll': None, 
                       'limit': 0, 
                       'printStats': False, 
                       'frame': None})
    registration_processor.registrationProcessor(options)

autoregister()