#! /usr/bin/env python
import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
from geocamTiePoint.viewHelpers import *
from geocamUtil import imageInfo

"""
For the special case where the image that rawImageData points to does not exist.
"""


def createNewImageData():
    names = ["ISS048-E-120.jpg", "iss045-E-106554.jpg", "ISS045-E-106552.jpg", "ISS044-E-48299.jpg", "ISS044-E-48298.jpg"]
    for name in names:
        overlay = Overlay.objects.get(name=name)
        alignedQT = overlay.alignedQuadTree
        try:
            gotImage = alignedQT.getImage()
        except: 
            try: 
                if overlay.extras.orgImageSize[0] < 1000:
                    sizeType = 'small'
                else: 
                    sizeType = 'large'
            except:
                continue 
            mission, roll, frame = overlay.name.split('.')[0].split('-')
            issImage = ISSimage(mission, roll, frame, sizeType)
            imageUrl = issImage.imageUrl
            # get image data from url
            imageFile = imageInfo.getImageFile(imageUrl)
            if checkIfErrorJSONResponse(imageFile):
                continue
            # delete the old raw image data that has a bad file
            overlay.getRawImageData().delete()
            # create a new one form the newly imnported image.
            rawImageData = createImageData(imageFile, sizeType)
            rawImageData.overlay = overlay
            rawImageData.save()
            if overlay.unalignedQuadTree.imageData is not None:
                overlay.unalignedQuadTree.imageData.delete()
            overlay.unalignedQuadTree.imageData = rawImageData
            if overlay.alignedQuadTree.imageData is not None:
                overlay.alignedQuadTree.imageData.delete()
            overlay.alignedQuadTree.imageData = rawImageData
            overlay.save()

createNewImageData()