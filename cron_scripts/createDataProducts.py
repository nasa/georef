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


def createDataProducts(opts):   
    '''
    Create exports for manually generated images.
    '''
    interval = int(opts.seconds)
    while True:
        time.sleep(interval)
        overlays = Overlay.objects.all()
        for overlay in overlays:
            if ('transform' in overlay.extras):
                if overlay.readyToExport:
                    # check if the output exists already
                    alignedQT = overlay.alignedQuadTree
                    if alignedQT: 
                        if bool(alignedQT.htmlExport) is False:
                            overlay.generateHtmlExport()
                        
                        if bool(alignedQT.geotiffExport) is False:
                            overlay.generateGeotiffExport()
                        # note: kml export depends on existence of geotiff export.
                        if bool(alignedQT.kmlExport) is False:
                            overlay.generateKmlExport()
                    
                        if alignedQT.metadataExportName is None:
                            try: 
                                createMetaDataFile(overlay)
                            except: 
                                continue
    

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
