#!/usr/bin/env python

import datetime

import django
from django.conf import settings
django.setup()

from georef_imageregistration import output_generator, registration_common
from geocamTiePoint import quadTree


def generateManualRegistrationOutput(opts):
    """
    Runs the registration_processor in georef_imageregistration app.
    """
    mission = None
    roll = None
    frame = None
    limit = 0
    autoOnly = False 
    manualOnly = True
    sleepInterval = opts.sleepInterval
    
    output_generator.runOutputGenerator(mission, 
                                        roll, 
                                        frame, 
                                        limit, 
                                        autoOnly, 
                                        manualOnly,
                                        sleepInterval)


def main():
    import optparse
    seconds = 30 * 60  # once it finishes, sleep for 30 minutes and try again.
    parser = optparse.OptionParser('usage:%prog')
    parser.add_option('-s', '--sleepInterval',
                      default= seconds,
                      help='sleep interval in seconds')
    opts, _args = parser.parse_args()
    generateManualRegistrationOutput(opts)


if __name__ == '__main__':
    main()