Installation
============

Requirements
~~~~~~~~~~~~

Our reference platform for GeoRef is Ubuntu Linux 14.04 LTS,
running Python 2.7.6 and Django 1.9.2.  For development we use Django's
built-in development web server with a SQLite 3.6 database.  

We develop using a VagrantBox VM running a Ubuntu Linux inside a Mac OS X host machine.
Vagrant VM is strictly optional and only necessary if you are not running directly from a Ubuntu Linux Machine.

Our image view is rendered using the OpenSeadragon open source image viewer. (openseadragon.github.io/)

(Optional) Set up a Vagrant VM
~~~~~~~~~~~~~~~~~~~~

Install VirtualBox. Make sure the version is 4.3.10.
Install the latest version of vagrant: ​http://www.vagrantup.com/downloads


Set Up an Install Location
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create a directory to hold the whole GeoRef installation
and capture the path in an environment variable we can use
in the instructions below::

  export GEOCAM_DIR=$HOME/projects/geocam # or choose your own
  mkdir -p $GEOCAM_DIR
  

Get the Source
~~~~~~~~~~~~~~

Check out our latest source revision with::

  cd $GEOCAM_DIR
  git clone https://babelfish.arc.nasa.gov/git/georef_deploy/

For more information on the Git version control system, visit `the Git home page`_.
You can install Git on Ubuntu with::

  sudo apt-get install git-all

.. _the Git home page: http://git-scm.com/


Run the Setup Script
~~~~~~~~~~~~~~~~~~~~~
	# go into the georef_deploy directory 
	cd georef_deploy
	
	# if you are running inside a Vagrant VM do
	setup_site_vagrant.sh
	
	OR 
	
	# if you are running directly on a Ubuntu Linux Machine, do
	sudo python $GEOCAM_DIR/georef_deploy/setup_site.py
		# You need to manually create couple symlinks if not running on vagrant.
		sudo ln -s /home/geocam/georef_deploy georef_deploy
		sudo ln -s gds/georef/ georef

The script should initialize the vagrant box and it clones all the submodules that are needed.


Install Non-Python Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

First install Ubuntu packages::

  # tools for Python package compilation and management
  sudo apt-get install python2.7-dev python-pip

  # database support for development in native django environment
  sudo apt-get install sqlite3 libsqlite3-dev

  # handling images
  sudo apt-get install libpng-dev libjpeg-dev libfreetype6-dev libtiff-dev imagemagick

  # must install PIL through Ubuntu package system, PyPI version fails on Ubuntu
  sudo apt-get python-imaging


Set Up GeoRef
~~~~~~~~~~~~~~~~

To install Python dependencies, render icons and collect media for the
server, run::

  cd $GEOCAM_DIR/georef
  ./manage.py bootstrap --yes
  source $GEOCAM_DIR/georef/sourceme.sh genSourceme genSettings
  ./manage.py prep

You'll need to source the ``sourceme.sh`` file every time you open a new
shell if you want to run GeoCam-related Python scripts such as starting
the Django development web server.  The ``sourceme.sh`` file will also
take care of activating your virtualenv environment in new shells (if
you were in a virtualenv when you ran ``setup.py``).

To initialize the database::

	$GEOCAM_DIR/georef/manage.py makemigrations geocamTiePoint
	$GEOCAM_DIR/georef/manage.py makemigrations georefApp
	$GEOCAM_DIR/georef/manage.py migrate


Try It Out
~~~~~~~~~~

Now you're ready to try it out!  Point your browser to ​http://10.0.3.18/


Override settings.py
~~~~~~~~~~~~~~~~~~~~~~~

In the ``settings.py`` file, modify the ``DATABASES`` field to point to
your Django MySQL database::

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'georef',
        'USER': 'root',
        'PASSWORD': 'vagrant',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

.. o  __BEGIN_LICENSE__
.. o  Copyright (C) 2008-2010 United States Government as represented by
.. o  the Administrator of the National Aeronautics and Space Administration.
.. o  All Rights Reserved.
.. o  __END_LICENSE__