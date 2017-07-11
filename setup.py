#__BEGIN_LICENSE__
# Copyright (c) 2017, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The GeoRef platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

import os
from setuptools import setup, find_packages, Command

import os.path as op
import subprocess


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

# Use the docstring of the __init__ file to be the description
#DESC = " ".join(__import__('geoRef').__doc__.splitlines()).strip()
DESC = ""

PROJ_ROOT = op.abspath(op.dirname(__file__))


def find_sub_apps(directory=PROJ_ROOT):
    """We define a sub-application to be any top-level subdirectory that
    contains a urls.py and a models.py. Note that we do not look solely
    for submodule based apps, since there could be an odd app or two that
    aren't based on a git submodule, or it could be the main 'glue'
    application."""
    requiredFiles = ['models.py', 'urls.py']
    subApps = []
    for entry in os.listdir(directory):
        fullEntry = op.join(directory, entry)
        if not op.isdir(fullEntry):
            continue
        if all([op.exists(op.join(fullEntry, f)) for f in requiredFiles]):
            subApps.append((entry, fullEntry))
    return subApps


def find_submodules(directory=op.join(PROJ_ROOT, 'apps')):
    """We define a submodule as a subdirectory in submodules which contains a
    subdirectory under that of the same name. We do not do git magic as there
    could be times where it is a sub-app that isn't a git subrepo."""
    subModules = []
    for entry in os.listdir(directory):
        fullEntry = op.join(directory, entry)
        if not op.isdir(fullEntry):
            continue
        fullSubDir = op.join(fullEntry, entry)
        if op.exists(fullSubDir) and op.isdir(fullSubDir):
            subModules.append((entry, fullSubDir))
    return subModules


class RunSubCommand(Command):
    """Run a sub-command on the sub-apps. This class is meant to be subclassed.
    Override 'self.subcommand' in initialize_options to specify what command
    to run. If you override run, be sure to call this class' run to
    run the subcommand."""
    user_options = []

    # Option defaults
    def initialize_options(self):
        self.subcommand = None  # pylint: disable=W0201

    # Validate options
    def finalize_options(self):
        pass

    # Where the action happens
    def run(self):
        if getattr(self, 'subcommand', None) is None:
            raise Exception("must override self.subcommand")
        projDir = op.abspath(op.dirname(__file__))
        subApps = find_sub_apps(projDir)
        for app, _directory in subApps:
            appDir = op.join(projDir, 'submodules', app)
            if not op.exists(appDir):
                self.announce("skipping %s" % app)
                continue

            setupPath = op.join(appDir, 'setup.py')
            if not op.exists(setupPath):
                self.announce("skipping %s" % app)
                continue

            subprocess.call(["python", setupPath, self.subcommand])


class TestCommand(RunSubCommand):
    description = 'test geocam command'
    user_options = []

    # Option defaults
    def initialize_options(self):
        self.subcommand = 'geocam'

    # Validate options
    def finalize_options(self):
        pass


class SymlinkCommand(Command):
    """This command makes the submodule app directories symlinked to the
    site-level. Will not work on windows."""
    description = 'symlink submodules to the main site level'
    user_options = [('force', 'f', 'overwrite existing symlinks')]
    boolean_options = ['force']

    # Option defaults
    def initialize_options(self):
        self.force = False

    # Validate options
    def finalize_options(self):
        pass

    def run(self):
        subModules = find_submodules()
        for name, directory in subModules:
            destination = op.join(PROJ_ROOT, name)
            if op.exists(destination):
                if not op.islink(destination):
                    self.announce("skipping " + name + ": not a symlink")
                    continue
                if not self.force:
                    self.announce("skipping " + name + ": file exists (use -f to override)")
                    continue
                os.remove(destination)
            os.symlink(directory, destination)


class MediaCommand(Command):
    description = 'collect together the site-level static media'
    user_options = [('force', 'f', 'overwrite existing symlinks')]
    boolean_options = ['force']

    # Option defaults
    def initialize_options(self):
        self.force = False

    # Validate options
    def finalize_options(self):
        pass

    def run(self):
        siteMediaDir = op.join(PROJ_ROOT, 'media')
        if not op.exists(siteMediaDir):
            os.mkdir(siteMediaDir)
        subApps = find_sub_apps()
        for name, directory in subApps:
            mediaDirectory = op.join(directory, 'media', name)
            if not op.exists(mediaDirectory):
                self.announce("skipping " + name + ": media directory does not exist")
                continue
            destination = op.join(siteMediaDir, name)
            if op.exists(destination):
                if not op.islink(destination):
                    self.announce("skipping " + name + ": not a symlink")
                    continue
                if not self.force:
                    self.announce("skipping " + name + ": file exists (use -f to override)")
                    continue
                os.remove(destination)
            os.symlink(directory, destination)


setup(
    name="geoRef",
    version='1.0',  # __import__('geoRef').get_version().replace(' ', '-'),
    url='',
    author='mfsmith3, ylee8',
    author_email='',
    description=DESC,
    long_description=read_file('README'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_file('requirements.txt'),
    classifiers=[
        'License :: OSI Approved :: NASA Open Source Agreement',
        'Framework :: Django',
    ],

    cmdclass={
        'link_submodules': SymlinkCommand,
        'link_media': MediaCommand
    },
)
