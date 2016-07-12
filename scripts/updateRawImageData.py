import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
DISPLAY = 2
ENHANCED = 1 
UNENHANCED = 0

"""
Image related stuff
"""

def getImage(imageData, flag):
    """
    Returns the PIL image object from imageData based on the flag.
    """
    image = None
    try: 
        if flag == ENHANCED:
            image = PIL.Image.open(imageData.enhancedImage.file)
        elif flag == UNENHANCED:
            image = PIL.Image.open(imageData.unenhancedImage.file)
        elif flag == DISPLAY:
            image = PIL.Image.open(imageData.image.file)
    except: 
        logging.error("image cannot be read from the image data")
        return None
    return image

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