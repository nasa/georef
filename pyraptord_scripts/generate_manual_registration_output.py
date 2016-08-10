#!/usr/bin/env python
import time
import datetime
import subprocess
import os.path
from os import listdir
import logging

import django
from django.conf import settings
django.setup()

from geocamTiePoint.models import *
from georef_imageregistration import offline_config, output_generator, registration_common, georefDbWrapper
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
    centerPointSource = None
    logging.info("inside createMetaDataFile")
    try: 
        successFrames, centerPointSource = output_generator.runOutputGenerator(mission, roll, frame, limit, autoOnly, manualOnly)
    except Exception as e:
        raise Exception('Exception in runOutputGenerator script') 
        return

    if len(successFrames) > 0:
        sourceFilesDir = registration_common.getWorkingDir(mission, roll, frame)
        zipFileDir = registration_common.getZipFilePath(mission, roll, frame)
        
        # bundle the files into a zip file.
        timenow = datetime.datetime.utcnow()
        zipFileName = issMRF + '_manual_' + timenow.strftime('%Y-%m-%d-%H%M%S-UTC') + '.zip'
        zipFilePath = zipFileDir + '/' + zipFileName
        
        writer = quadTree.ZipWriter(sourceFilesDir, zipFilePath)
        frame = issMRF.split('-')[2]
        centerPointSource = georefDbWrapper.MANUAL
        writer.addDir(frame, centerPointSource)
        
        # save the zipfile name to the quad tree. 
        alignedQT.metadataExportName = zipFileName
        alignedQT.save()
        
        overlay.writtenToFile = True
        overlay.save()
        logging.info("overlay is saved.")
        

def generateManualRegistrationOutput():
    """
    Creates output products for manually registered images (ones done with GeoRef UI) 
    """
    logging.info("inside the pyraptord script, generate manual registration output")
    overlays = Overlay.objects.all()
    for overlay in overlays:
        if ('transform' in overlay.extras) and (len(overlay.extras.points) > 2):
            if overlay.readyToExport:
                alignedQT = overlay.alignedQuadTree
                # check if the output exists already
                if alignedQT.metadataExportName is None:
                    try: 
                        createMetaDataFile(overlay)
                    except Exception, e: 
                        print str(e)
                        continue


def main():
    generateManualRegistrationOutput()


if __name__ == '__main__':
    main()