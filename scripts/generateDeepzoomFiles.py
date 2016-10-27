#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


def generateDeepzoomFiles():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        if overlay.imageData is not None:
            # set the contrast value to 1
            overlay.imageData.contrast = 1
            overlay.imageData.brightness = 0
            overlay.imageData.rotationAngle = 0
            overlay.imageData.save()
            # create deepzoom files
            try: 
                if overlay.imageData.associated_deepzoom is None: 
                    dz = overlay.imageData.create_deepzoom_image()
            except: 
                print "could not create deepzoom file for overlay %s" % overlay.name
            
generateDeepzoomFiles()