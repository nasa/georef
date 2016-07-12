import django
django.setup()

from django.conf import settings
settings.configure()

from geocamTiePoint.models import *
from geocamTiePoint.viewHelpers import *

def updateRawImageData():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        rdata = overlay.getRawImageData()
        if rdata.issMRF is None:
            rdata.issMRF = overlay.name.split('.')[0]
            if rdata.unenhancedImage.name == '1':
                rdata.unenhancedImage = rdata.image
            if (rdata.width == 0) or (rdata.height == 0): 
                image = getImage(rdata, DISPLAY)
                size = image.size
                rdata.width = size[0]
                rdata.height = size[1]
                imgSize = "large"
                if width < 1200:
                    imgSize = "small"
                rdata.sizeType = imgSize
            rdata.save() 