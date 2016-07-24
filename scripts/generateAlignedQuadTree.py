#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *


"""
Adds image width, height, sizeType fields to Image Data (previously was in overlay.extras)
"""
def generateAlignedQuadTree():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        if overlay.alignedQuadTree is None:
            overlay.generateAlignedQuadTree()
            overlay.save()
            
generateAlignedQuadTree()