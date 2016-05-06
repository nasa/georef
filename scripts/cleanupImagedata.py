import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
from geocamUtil import imageInfo
from geocamTiePoint.viewHelpers import *
from django.conf import settings

import sys
print sys.argv

"""
//0. add a sizeType field to imageData model and migrate 
1. compile a list of all used imageData
    for each overlay -> overlay.imageData and overlay.getRawImageData (make sure no dupes)
2. compile a list of all used quadtrees
    for each overlay-> overlay.unalignedQtree / alignedQtree. 
    for each used imageData, search for corresponding quad tree QuadTree(imageData__key = self.key)
    make sure there are no dupes

3. loop through image imageData,
    make sure it's in the used ImageData list, if not, delete (DO THIS ON A COPY: AND delete its image / unenhancedImage/ enhancedImage!!!)
    
4. loop through quad trees, if it's not in a used quad tree list, delete. 

"""


def listUsedImageData():
    imageDataList = []
    overlays = Overlay.objects.all()
    for overlay in overlays:
        try: 
            imageDataList.append(overlay.imageData.id)
        except:
            print "overlay %s has no image data" % overlay.name
        try: 
            imageDataList.append(overlay.getRawImageData().id)
        except:
            print "overlay %s has no raw image!" % overlay.name
    return list(set(imageDataList))


def listUsedQuadTrees():
    qtreeList = []
    overlays = Overlay.objects.all()
    imdList = listUsedImageData()
    for overlay in overlays: 
        try: 
            qtreeList.append(overlay.unalignedQuadTree.id)
        except:
            pass
        try: 
            qtreeList.append(overlay.alignedQuadTree.id)
        except: 
            pass
    for imd in imdList:
        try: 
            qtreeList.append(Quadtree.objects.get(imageData = imd).id)
        except:
            pass
    return list(set(qtreeList))
        

def listUsedImages():
    goodImages = []
    goodImageData = listUsedImageData()
    for imdata_id in goodImageData:
        imageData = ImageData.objects.get(id=imdata_id)
        try: 
            goodImages.append(imageData.image.name.split('/')[-1])
        except:
            pass
        try: 
            goodImages.append(imageData.unenhancedImage.name.split('/')[-1])
        except:
            pass
        try: 
            goodImages.append(imageData.unenhancedImage.name.split('/')[-1])
        except:
            pass
    return list(set(goodImages))


"""
Main functions
"""

def cleanupImageData():
    goodImageData = listUsedImageData()
    allImdata = ImageData.objects.all()
    for imdata in allImdata:
        print "image data %d" % imdata.id
        if imdata.id not in goodImageData:
            print "%d deleted" % imdata.id
            imdata.delete()


def cleanupQuadTrees():
    goodQtrees = listUsedQuadTrees()
    allQtrees = QuadTree.objects.all()
    for qtree in allQtrees:
        print "qtree %d" % qtree.id
        if qtree.id not in goodQtrees:
            print "%d deleted" % qtree.id
            qtree.delete()


def cleanupImageFiles():
    # get all the image file names stored in good image data.
    #goodImageData = listUsedImageData()

    #list all files in the data directory
    from os import listdir
    from os.path import isfile, join
    
    goodImages = listUsedImages()
    print "good images are"
    print goodImages
    mypath = '/home/geocam/georef/data/geocamTiePoint/overlay_images'
#     mypath = '/home/vagrant/gds/georef/data/geocamTiePoint/overlay_images'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles: 
        print "file name %s" % file
        if file not in goodImages:
            print "%s deleted" % file
            os.remove(mypath + '/' + file)
            

def createRawImageData():
    overlays = Overlay.objects.all()
    for overlay in overlays:
        try: 
            mission, roll, frame = overlay.name.split('.')[0].split('-')
        except:
            continue
        raw = overlay.getRawImageData()
        if not raw:
            print "no raw imagedata exists for overlay %d" % overlay.pk 
            oldImageData = overlay.imageData
            sizeType = None
            if oldImageData.image.size < 600000:
                sizeType = 'small'
            else: 
                sizeType = 'large'
            issImage = ISSimage(mission, roll, frame, sizeType)
            imageUrl = issImage.imageUrl
            # get image data from url
            imageFile = imageInfo.getImageFile(imageUrl)
            rawImageData, imageSize = createImageData(imageFile)
            print "new raw imagedata %d saved for overlay %d" % (rawImageData.id, overlay.pk)
            rawImageData.overlay = overlay
            rawImageData.save()



def __main__():
    arg1 = sys.argv[1]
    if arg1 == '1':
        cleanupImageData()
    elif arg1 == '2':
        cleanupQuadTrees()
    elif arg1 == '3':
        cleanupImageFiles()
    elif arg1 == '4':
        createRawImageData()
    else:
        print "Wrong argument. Either needs to be 1 2 or 3"
        pass # do nothing

__main__()

# def buildQuadTreeImageDictionary():
#     """
#     Builds a dict that maps a used (by overlay) quadtree id to issMRF
#     """
#     dict = {} # key is quad tree id, value is issMRF
#     overlays = Overlay.objects.all()
#     for overlay in overlays:
#         dict[overlay.unalignedQuadTree.id] = overlay.imageData.issMRF
#         dict[overlay.alignedQuadTree.id] = overlay.imageData.issMRF
# 
#     return dict
# 
# def cleanupQuadTrees():
#     """
#     Deletes unused quad tree objects
#     """
#     dict = buildQuadTreeImageDictionary()
#     qtrees = QuadTree.objects.all()
#     for tree in qtrees:
#         if tree.id not in dict.keys():
#             tree.delete()
# 
# 
# def cleanupImageData():
#     overlays = Overlay.objects.all()
#     for overlay in overlays:
#         overlay.getRawImageData()
# 
# def generateImageData():
#     for overlay in overlays:
#         issID = overlay.name.split('.')[0].split('-')
#         mission = issID[0]
#         roll = issID[1]
#         frame = issID[2]
#         issImage = ISSimage(mission, roll, frame, sizeType)
#         imageUrl = issImage.imageUrl
#         imageFile = imageInfo.getImageFile(imageUrl)

