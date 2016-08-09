#!/usr/bin/env python
import django
from django.conf import settings
django.setup()

from georef_imageregistration import output_generator


def generateAutoregistrationOutput():
    """
    Runs the registration_processor in georef_imageregistration app.
    """
    mission = None
    roll = None
    frame = None
    limit = 0
    autoOnly = True 
    manualOnly = False
    successFrames = output_generator.runOutputGenerator(mission, roll, frame, limit, autoOnly, manualOnly)

#     # zip up the processed files
#     for frame in successFrames:
#         [(u'ISS039', u'E', u'12427')]
        
    

generateAutoregistrationOutput()