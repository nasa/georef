#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


"""
Adds image width, height, sizeType fields to Image Data (previously was in overlay.extras)
"""
def markReadyToExport():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        if 'transform' in overlay.extras:
            overlay.readyToExport = True
            overlay.save()

markReadyToExport()