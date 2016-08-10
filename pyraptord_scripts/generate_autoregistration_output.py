#!/usr/bin/env python

import datetime

import django
from django.conf import settings
django.setup()

from georef_imageregistration import output_generator, registration_common
from geocamTiePoint import quadTree

def generateAutoregistrationOutput():
    """
    Runs the registration_processor in georef_imageregistration app.
    """
    mission = None
    roll = None
    frame = None
    limit = 0
    autoOnly = True 
    manualOnly = False
    successFrames, centerPointSources = output_generator.runOutputGenerator(mission, roll, frame, limit, autoOnly, manualOnly)

    index = 0
    for mrf in successFrames:
        mission, roll, frame = mrf
        timenow = datetime.datetime.utcnow()
        centerPointSource = centerPointSources[index]
        # define the path where zipfile will be saved
        zipFileName = mission + '-' + roll + '-' + frame + '_' + centerPointSource + '_' + timenow.strftime('%Y-%m-%d-%H%M%S-UTC') + '.zip'
        zipFileDir = registration_common.getZipFilePath(mission, roll, frame)
        zipFilePath = zipFileDir + '/' + zipFileName 
        # geotiff images and metadata files to be zipped
        sourceFilesDir = registration_common.getWorkingDir(mission, roll, frame)
        
        writer = quadTree.ZipWriter(sourceFilesDir, zipFilePath)
        writer.addDir(frame, centerPointSource)
        index = index + 1

generateAutoregistrationOutput()