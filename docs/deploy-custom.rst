Deployment on a custom machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prerequisites
=============

You will need the following:

* A clone of the git repository at ``https://github.com/political-memory/political_memory.git``
* A dedicated python virtualenv
* a PostgreSQL>=9.2 database (not necessarily on the same machine)
* a WSGI-capable web server

Setup environment
=================

Set the following environment variables::

    DJANGO_SETTINGS_MODULE=memopol.settings

Customize settings
==================

Create a copy of the example local settings file::

    $ cp src/memopol/local_settings.py.example src/memopol/local_settings.py

Edit ``src/memopol/local_settings.py`` to set directories, database settings and
allowed hosts.  Setup your WSGI server to serve:

* Static files from the directory specified in the ``PUBLIC_DIR`` setting to the
  ``/static`` URL
* The ``src/memopol/wsgi.py`` WSGI application

Initial memopol setup
=====================

From the repository root, install python dependencies (you may want to do that
in a virtualenv)::

    $ pip install -U pip setuptools
    $ pip install -Ue .

Install client libraries::

    $ src/memopol/bin/install_client_deps.sh

Setup the database schema::

    $ memopol migrate --noinput

Collect static files::

    $ memopol collectstatic --noinput

Memopol should be ready to go.

Updating
========

To update simply pull the repository and run setup commands again::

    $ git pull
    $ pip install -Ue .
    $ src/memopol/bin/install_client_deps.sh
    $ memopol migrate --noinput
    $ memopol collectstatic --noinput

Data provisionning
==================

Set up two cron jobs:

* One to update data from parliaments, that runs ``bin/update_all``.  This
  script takes quite some time to run, so you should schedule it once every
  night for example
* One to refresh scores,  that runs ``memopol refresh_scores``.  This one
  runs quite quickly (a few seconds), you may want to run it after the update
  job has completed (but you can run it more often).

Ensure that cron jobs get the same environment as the application.


Continue to :doc:`administration`.
