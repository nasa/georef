#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import Overlay


def moveCenterPtOutOfExtras():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        overlay.centerLat = overlay.extras.centerLat
        overlay.centerLon = overlay.extras.centerLon
        overlay.nadirLat = overlay.extras.nadirLat
        overlay.nadirLon = overlay.extras.nadirLon
        overlay.save()
moveCenterPtOutOfExtras()