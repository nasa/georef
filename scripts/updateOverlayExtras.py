#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import Overlay, ISSimage
from geocamUtil import registration as register

def updateOverlayExtras():
    """
    This is a standalone method used to update the contents of overlay extras, 
    which has changed to reflect the new UI for list overlays page.
    """
    overlays = Overlay.objects.all()
    for overlay in overlays:
#         if overlay.extras.imageSize[0] > 1000:
#             imageSize = 'large'
#         else: 
#             imageSize = 'small'

        #already existing (get id from overlay name and put it into extras and imagedata)
        if (hasattr(overlay.extras, 'issMRF') and (overlay.extras['issMRF'] is not None)):
            overlay.imageData.issMRF = overlay.extras['issMRF']
        else: 
            overlay.imageData.issMRF = overlay.name.split('.')[0]    
        overlay.imageData.save()
        overlay.save()
#             issMRF = issMRF.split('-')
#             mission = issMRF[0]
#             roll = issMRF[1]
#             frame = issMRF[2]   
#             issImage = ISSimage(mission, roll, frame, imageSize)
#             centerPtDict = register.getCenterPoint(issImage)
#             try:
#                 overlay.extras.centerLat = round(centerPtDict["lat"],2)
#                 overlay.extras.centerLon = round(centerPtDict["lon"],2)
#             except:
#                 overlay.extras.centerLat = None
#                 overlay.extras.centerLon = None
#             overlay.extras.nadirLat = issImage.extras.nadirLat
#             overlay.extras.nadirLon = issImage.extras.nadirLon
#             ad = issImage.extras.acquisitionDate
#             overlay.extras.acquisitionDate = ad[:4] + ':' + ad[4:6] + ':' + ad[6:] # convert YYYYMMDD to YYYY:MM:DD 
#             at = issImage.extras.acquisitionTime
#             overlay.extras.acquisitionTime = at[:2] + ':' + ad[2:4] + ':' + ad[4:6] # convert HHMMSS to HH:MM:SS
#             overlay.extras.focalLength_unitless = issImage.extras.focalLength_unitless
#             overlay.save()
updateOverlayExtras()