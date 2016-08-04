#!/usr/bin/env python
import time
import datetime
import subprocess
import os.path
from os import listdir

import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
from georef_imageregistration import offline_config, output_generator, registration_common
from geocamTiePoint import quadTree


"""
This script only works for manually generated images. It creates the metadata file, and the data products
for the ones that were manually registered in GeoRef. 
TODO: write a script for auto-generated images.
"""

def createMetaDataFile(overlay):                    
    """
    Creates the metadata file using Scott's code, and returns the full path of the tar file. 
    """
    alignedQT = overlay.alignedQuadTree
    issMRF = overlay.getRawImageData().issMRF
    mission, roll, frame = issMRF.split('-')
    
    limit = 0
    autoOnly = False
    manualOnly = True
    successFrames = []
    try: 
        successFrames = output_generator.runOutputGenerator(mission, roll, frame, limit, autoOnly, manualOnly)
    except: 
        raise Exception('Exception in runOutputGenerator script') 
        return

    if len(successFrames) > 0:
        outputDirFullPath = os.path.dirname(registration_common.getWorkingPath(mission, roll, frame))
        allFiles = os.listdir(outputDirFullPath)
        # bundle the files into the tar.gz
        exportTarballName = issMRF + '_geotiffs_with_metadata'
        writer = quadTree.TarWriter(exportTarballName)
        for filename in allFiles: 
            if frame in filename:  # only grab the ones that have the same frame number
                fullPath = outputDirFullPath + '/' + filename
                writer.addFile(fullPath, filename)
    
        alignedQT.metadataExportName = '%s.tar.gz' % exportTarballName
        alignedQT.metadataExport.save(alignedQT.metadataExportName, 
                                      ContentFile(writer.getData()))
        alignedQT.save()
        
        overlay.writtenToFile = datetime.datetime.utcnow()
        overlay.save()


# measure process time
t0 = time.clock()
procedure()
print time.clock() - t0, "seconds process time"

def createDataProducts(opts):   
    '''
    Create exports for manually generated images.
    '''
#     interval = int(opts.seconds)
#     while True:
#         time.sleep(interval)
#     overlays = Overlay.objects.all()
    overlay = Overlay.objects.get(name="ISS045-E-106553.jpg")
#    for overlay in overlays:
    if ('transform' in overlay.extras) and (len(overlay.extras.points) > 2):
        if overlay.readyToExport:
            # check if the output exists already
            alignedQT = overlay.alignedQuadTree
            try:  # handle the case where the image is missing from the imagedata in alignedQuadTree.
                imageFile = overlay.alignedQuadTree.imageData.image.file
            except: 
                try:
                    overlay.alignedQuadTree.imageData = overlay.getRawImageData()
                    overlay.alignedQuadTree.save()
                except: 
                    pass
#                     continue
            if alignedQT: 
                if bool(alignedQT.htmlExport) is False:
                    t0 = time.clock()
                    overlay.generateHtmlExport()
                    print "generate Html export"
                    print time.clock() - t0
                if bool(alignedQT.geotiffExport) is False:
                    t0 = time.clock()
                    overlay.generateGeotiffExport()
                    print "generate geotiff export"
                    print time.clock() - t0
                # note: kml export depends on existence of geotiff export.
                if bool(alignedQT.kmlExport) is False:
                    t0 = time.clock()
                    overlay.generateKmlExport()
                    print "generate kml export"
                    print time.clock() - t0
                if alignedQT.metadataExportName is None:
                    t0 = time.clock()
                    try:  # TODO: I can have this return the name of the Geotiff, and then run generate KML.
                        createMetaDataFile(overlay)
                    except: 
                        pass
                    print "generate metadata export"
                    print time.clock() - t0
#                         continue

def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog')
    parser.add_option('-s', '--seconds',
                      default="",
                      help='second interval to check for new data')
    opts, _args = parser.parse_args()
    createDataProducts(opts)


if __name__ == '__main__':
    main()
