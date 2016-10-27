#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


import time


def generateDeepzoomFiles():
    overlays = Overlay.objects.all()
    
    start = time.time()
    count = 0
    for overlay in overlays:
        
        if overlay.imageData is not None:
            count = count + 1
            dstart = time.time()
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
            dend = time.time()
            print "deepzoom creation time:"
            print (dend - dstart)
            
    end = time.time()
    print "***************************************"
    print("Total time for deepzoom creation.")
    print(end - start)
    print "total number of overlays"
    print count
            
generateDeepzoomFiles()