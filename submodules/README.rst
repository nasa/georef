This Django site uses git submodules to pull in closely related packages
from external git repositories. 

Conventions
===========

Submodules should be cloned into this ``submodules`` directory.

If a submodule requires that external Python modules be installed, they
should be listed in a file named ``requirements.txt`` in that
submodule's top-level directory. Initializing the site (``./manage.py
prep``) will install the requirements with ``pip``.

For submodules that define Django apps, the directory within the
submodule that defines the app (the one that contains the ``models.py``
file) should be symlinked into the ``apps`` directory, which is in the
``PYTHONPATH`` for the site.  For example, ``apps/geocamUtil`` might be
a symlink to ``submodules/geocamUtilWeb/geocamUtil``. (In some cases, a
single submodule might define multiple apps which are separately
symlinked into the ``apps`` directory.)

Example of Adding a New Submodule
=================================
::

  cd georef
  # note: using public (read-only) submodule URL to allow devs without
  # write access to fetch submodule
  git submodule add git://github.com/geocam/geocamUtilWeb.git submodules/geocamUtilWeb
  ln -s ../submodules/geocamUtilWeb/geocamUtil apps/geocamUtil
  git add apps/geocamUtil # check the symlink into git
  git commit -m 'added geocamUtil app'
