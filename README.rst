Installation
============

Requirements
~~~~~~~~~~~~

Our reference platform for GeoCam MapFasten is Ubuntu Linux 12.04 LTS,
running Python 2.7.3 and Django 1.3.  For development we use Django's
built-in development web server with a SQLite 3.6 database.  We also
develop using Mac OS X 10.6+ but we won't talk about how to install
dependencies on the Mac since it's more complicated.

For deployment we deploy to Google App Engine, using Google Cloud SQL
for the database and App Engine blob storage to hold image data.

Set Up an Install Location
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create a directory to hold the whole MapFasten installation
and capture the path in an environment variable we can use
in the instructions below::

  export GEOCAM_DIR=$HOME/projects/geocam # or choose your own
  mkdir -p $GEOCAM_DIR

Get the Source
~~~~~~~~~~~~~~

Check out our latest source revision with::

  cd $GEOCAM_DIR
  git clone git://github.com/geocam/geocamMapFasten.git geocamMapFasten

For more information on the Git version control system, visit `the Git home page`_.
You can install Git on Ubuntu with::

  sudo apt-get install git-core

.. _the Git home page: http://git-scm.com/

Optionally Install virtualenv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Especially for a quick test install, we recommend using the
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_
tool to put GeoCam-related Python packages in an isolated sandbox where
they won't conflict with other Python tools on your system.

To install virtualenv, create a sandbox named ``packages``, and
"activate" the sandbox::

  sudo apt-get install python-virtualenv
  cd $GEOCAM_DIR
  mkdir virtualenv
  cd virtualenv
  virtualenv --system-site-packages geocamMapFasten
  source geocamMapFasten/bin/activate

After your sandbox is activated, package management tools such as
``easy_install`` and ``pip`` will install packages into your sandbox
rather than the standard system-wide Python directory, and the Python
interpreter will know how to import packages installed in your sandbox.

You'll need to source the ``activate`` script every time you log in
to reactivate the sandbox.

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

Set Up MapFasten
~~~~~~~~~~~~~~~~

To install Python dependencies, render icons and collect media for the
server, run::

  cd $GEOCAM_DIR/geocamMapFasten
  ./manage.py bootstrap --yes
  source $GEOCAM_DIR/geocamMapFasten/sourceme.sh
  ./manage.py prep

You'll need to source the ``sourceme.sh`` file every time you open a new
shell if you want to run GeoCam-related Python scripts such as starting
the Django development web server.  The ``sourceme.sh`` file will also
take care of activating your virtualenv environment in new shells (if
you were in a virtualenv when you ran ``setup.py``).

To initialize the database::

  $GEOCAM_DIR/geocamMapFasten/manage.py syncdb

Try It Out
~~~~~~~~~~

To run the Django development web server::

  $GEOCAM_DIR/geocamMapFasten/manage.py runserver 0.0.0.0:8000

Now you're ready to try it out!  Point your browser to http://localhost:8000/ .

Deploying to App Engine
~~~~~~~~~~~~~~~~~~~~~~~

These instructions are a work in progress. Your feedback is appreciated!

Create an App Engine project, give it access to a Google Cloud SQL
instance, and enable backend support.

Change the ``application`` field in ``app.yaml`` to the name of your App
Engine project.

In the ``settings.py`` file, modify the ``DATABASES`` field to point to
your Cloud SQL database::

  DATABASES = {
      'default': {
          'ENGINE': 'google.appengine.ext.django.backends.rdbms',
          'INSTANCE': 'your cloud sql instance name',
          'NAME': 'your database name',
      }
  }

App Engine Python uses the ``appcfg.py`` script to upload your
application to the App Engine servers. For testing purposes, you'll
probably want to have development, staging, and deployment versions of
your app. We handle this by always giving ``appcfg.py`` an explicit
``--version`` argument at the command line which overrides the
``version`` setting in ``app.yaml``.

Note that by default all versions of your app will share the same
backend called ``processing`` which is used to produce export archives.
They will also share the same Cloud SQL database and blob storage
instance as the live deployed version. Use caution!

To deploy, run::

  cd $GEOCAM_DIR/geocamMapFasten
  appcfg.py --oauth2 --version=$MYVERSION update .
  appcfg.py --oauth2 backends . update processing

You should now be able to try out your app at http://yourapp.appspot.com/ .

.. o  __BEGIN_LICENSE__
.. o  Copyright (C) 2008-2010 United States Government as represented by
.. o  the Administrator of the National Aeronautics and Space Administration.
.. o  All Rights Reserved.
.. o  __END_LICENSE__
