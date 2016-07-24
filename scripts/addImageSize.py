#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


"""
Adds image width, height, sizeType fields to Image Data (previously was in overlay.extras)
"""
def addImageSize():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        width = overlay.extras.imageSize[0]
        height = overlay.extras.imageSize[1]
        imgSize = "large"
        if width < 1200:
            imgSize = "small"
        imageData = overlay.imageData   
        imageData.width = width
        imageData.height = height
        imageData.sizeType = imgSize
        imageData.save()
        
        # delete the extra fields (test this)
        del overlay.extras.imageSize
        overlay.save()
    
addImageSize()