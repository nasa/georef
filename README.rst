Installation
============

Requirements
~~~~~~~~~~~~

Our reference platform for GeoRef is Ubuntu Linux 14.04 LTS,
running Python 2.7.6 and Django 1.9.2.  For development we use Django's
built-in development web server MySQL database.  

We develop using a VagrantBox VM running a Ubuntu Linux inside a Mac OS X host machine.
Vagrant VM is strictly optional and only necessary if you are not running directly from a Ubuntu Linux Machine.

Our image view is rendered using the OpenSeadragon open source image viewer. (openseadragon.github.io/)

(Optional) Set up a Vagrant VM
~~~~~~~~~~~~~~~~~~~~
If you are running on a mac, we highly encourage you to use Vagrant to set up 
a Ubuntu Development Instance. Our set up script works best within the Vagrant 
environment running on Mac OSX.

Install VirtualBox. We have found that VirtualBox Version 4.3.10 works best with Vagrant.
We highly recommend you download VirtualBox 4.3.10.
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
  git clone https://github.com/nasa/georef_deploy.git


For more information on the Git version control system, visit `the Git home page`_.
You can install Git on Ubuntu with::

  sudo apt-get install git-all

.. _the Git home page: http://git-scm.com/


Run the Setup Script
~~~~~~~~~~~~~~~~~~~~~
The "setup_site_vagrant.sh" script initializes the vagrant box and it clones 
all the submodules that are needed::

    # go into the georef_deploy directory
    cd georef_deploy
    
    # if you are running inside a Vagrant VM do
    setup_site_vagrant.sh


If you are running directly on a Ubuntu Linux Machine, you can skip the above shell
script and run the following::
    sudo python $GEOCAM_DIR/georef_deploy/setup_site.py
    
    # You need to manually create couple symlinks if not running on vagrant
    sudo ln -s /home/geocam/georef_deploy georef_deploy
    sudo ln -s gds/georef/ georef


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


Setup the Data Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~
You must manually create the data directory and its sub folders. GeoRef will 
write the image tiles to this directory.

1. Create a data directory
    ``mkdir $GEOCAM_DIR/georef/data``
2. Create the overlays directory
    ``mkdir -p $GEOCAM_DIR/georef/data/geocamTiePoint/overlay_images``
3. Set the permissions
    ``chmod -R 777 $GEOCAM_DIR/georef/data``


Setup GeoRef
~~~~~~~~~~~~

If your development environment is set up inside Vagrant, cd into the georef_deploy 
directory and do::
    vagrant ssh
And then run the following commands.


You must create the following directory and files::

 # If you are not using Vagrant, do
     mkdir -p $GEOCAM_DIR/georef_deploy/georef/data/deepzoom/ & touch $GEOCAM_DIR/georef_deploy/georef/data/deepzoom/deepzoom.exception.log

 # If you are using Vagrant, do
     # deepzoom directory needs to be owned by www-data. Put it in /home/vagrant so that it can be owned by www-data (and not by user)
     mkdir -p /home/vagrant/deepzoom 
     # create a symlink to deepzoom in the data dir
     ln -s /home/vagrant/deepzoom /home/vagrant/georef/data/deepzoom


Install Earth Engine by following the instructions below: 
    https://developers.google.com/earth-engine/python_install_manual


To install Python dependencies, render icons and collect media for the
server, run::

  cd $GEOCAM_DIR/georef_deploy/georef
  ./manage.py bootstrap --yes
  source $GEOCAM_DIR/georef_deploy/georef/sourceme.sh genSourceme genSettings
  ./manage.py collectstatic  
  ./manage.py prep

You'll need to source the ``sourceme.sh`` file every time you open a new
shell if you want to run GeoCam-related Python scripts such as starting
the Django development web server.  The ``sourceme.sh`` file will also
take care of activating your virtualenv environment in new shells (if
you were in a virtualenv when you ran ``setup.py``).


To initialize the database
    ``$GEOCAM_DIR/georef/manage.py makemigrations deepzoom``

    ``$GEOCAM_DIR/georef/manage.py makemigrations geocamTiePoint``

    ``$GEOCAM_DIR/georef/manage.py migrate``

Note that the path to manage.py may be different if you are running inside Vagrant.


Create a User Account  
~~~~~~~~~~~~~~~~~~~~~
User name and password are required to use GeoRef. To create one, do::
    
    ./manage.py createsuperuser

And follow the prompts.



Try It Out
~~~~~~~~~~
Now you're ready to try it out!  

Restart the Apache server ``sudo apachectl restart``

Point your browser to ​http://10.0.3.18/


.. o  __BEGIN_LICENSE__
.. o  Copyright (C) 2008-2010 United States Government as represented by
.. o  the Administrator of the National Aeronautics and Space Administration.
.. o  All Rights Reserved.
.. o  __END_LICENSE__
