#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


"""
Adds image width, height, sizeType fields to Image Data (previously was in overlay.extras)
"""
def updateAcqDate():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        acqDate = overlay.extras.acquisitionDate
        if acqDate:
            try: 
                overlay.extras.acquisitionDate = acqDate.replace(':', '/')
            except:
                continue
            overlay.save()
    
updateAcqDate()