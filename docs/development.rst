Local development tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warn:: I reverse-engineered this from the source code I inherited, I might
          not be doing the right way nor be able to defend all of technical
          decisions.

This tutorial drives through a local installation of the project for
development on Linux. It requires git, a fairly recent version of python2 and
virtualenv.

Quickstart
==========

There is a quickstart script used and tested manually by some of the
developers. Feel free to try it, but don't worry if it doesn't work for you
then you can do each install step manually, which is recommended because well
that's how you will learn most.

Here's how to try it::

    $ git clone https://github.com/political-memory/political_memory.git
    $ cd political_memory
    $ source bin/quickstart.sh

If you want more control or if it doesn't work for you, then follow the steps
below or have a look at what the quickstart script does.

Make a virtual environment
==========================

For the sake of the tutorial, we'll do this in the temporary directory, but you
could do it anywhere::

    $ cd /tmp

Create a python virtual environment and activate it::

    $ virtualenv memopol_env
    Using real prefix '/usr'
    New python executable in memopol_env/bin/python2
    Also creating executable in memopol_env/bin/python
    Installing setuptools, pip, wheel...done.

    $ source memopol_env/bin/activate

Alternatively, use the tox command::

    $ tox -e py27
    $ source .tox/py27/bin/activate

Clone the repository
====================

You should fork the project on github and use the fork's clone url. For the
sake of the demo, we'll use the main repository URL::

    $ git clone https://github.com/political-memory/political_memory.git
    Cloning into 'political_memory'...
    remote: Counting objects: 2516, done.
    remote: Compressing objects: 100% (109/109), done.
    remote: Total 2516 (delta 44), reused 0 (delta 0), pack-reused 2402
    Receiving objects: 100% (2516/2516), 4.40 MiB | 79.00 KiB/s, done.
    Resolving deltas: 100% (1103/1103), done.
    Checking connectivity... done.

    $ cd political_memory/

Create your own branch, ie::

    $ git checkout -b yourbranch origin/pr
    Branch yourbranch set up to track remote branch pr from origin.
    Switched to a new branch 'yourbranch'

Install Python dependencies
===========================

Then, install the package for development::

    $ pip install -e .
    Obtaining file:///tmp/political_memory
    Collecting django (from political-memory==0.0.1)
      Using cached Django-1.9-py2.py3-none-any.whl

    [output snipped for readability]

    Installing collected packages: django, sqlparse, django-debug-toolbar, django-pdb, six, django-extensions, werkzeug, south, pygments, markdown, hamlpy, django-coffeescript, ijson, python-dateutil, pytz, political-memory
      Running setup.py develop for political-memory
    Successfully installed django-1.9 django-coffeescript-0.7.2 django-debug-toolbar-1.4 django-extensions-1.5.9 django-pdb-0.4.2 hamlpy-0.82.2 ijson-2.2 markdown-2.6.5 political-memory pygments-2.0.2 python-dateutil-2.4.2 pytz-2015.7 six-1.10.0 south-1.0.2 sqlparse-0.1.18 werkzeug-0.11.2

Install client dependencies
===========================

We'll also need to download client libraries::

    $ bin/install_client_deps.sh
    * Downloading jquery/jquery (2.1.4) from Github...
    * Downloading FortAwesome/Font-Awesome (v4.3.0) from Github...
    * Downloading lipis/flag-icon-css (0.7.1) from Github...
    * Downloading twbs/bootstrap (v3.3.5) from Github...
    * Done

Activate ``DJANGO_DEBUG``
=========================

``DEBUG`` is disabled by default, the development server
won't run properly by default thnen, to enable it export
the ``DJANGO_DEBUG`` variable in the current shell::

    $ export DJANGO_DEBUG=True

Setup the database
==================

Memopol requires PostgreSQL 9.1 or higher.  It used to run with SQLite, too, but
that is no longer the case.  Memopol uses the following environment variables
for database access:

* ``MEMOPOL_DB_NAME`` (defaults to 'memopol')
* ``MEMOPOL_DB_USER`` (defaults to 'memopol')
* ``MEMOPOL_DB_PASSWORD`` (defaults to 'memopol')
* ``MEMOPOL_DB_HOST`` (defaults to 'localhost')
* ``MEMOPOL_DB_PORT`` (defaults to '5432')

Make sure the corresponding user and database exist on your system; the user
will need the 'createdb' permission in order to be able to run tests.  To create
them, you may use the following commands::

    $ psql -c "create user memopol with password 'memopol';" -U postgres
    $ psql -c "alter role memopol with createdb;" -U postgres
    $ psql -c "create database memopol with owner memopol;" -U postgres

Database migrations
===================

Database migrations ensure the database schema is up to date with the project.
If you're not sure, you can run them anyway, they won't do any harm.  Use the
following command::

    $ memopol migrate
    Operations to perform:
      Synchronize unmigrated apps: django_filters, staticfiles, datetimewidget, autocomplete_light, messages, adminplus, compressor, humanize, django_extensions, constance, bootstrap3
      Apply all migrations: legislature, votes, database, admin, positions, sessions, representatives, auth, contenttypes, representatives_votes, taggit
    Synchronizing apps without migrations:
      Creating tables...
        Running deferred SQL...
      Installing custom SQL...
    Running migrations:
      Rendering model states... DONE
      Applying contenttypes.0001_initial... OK

    [output snipped for readability]

      Applying taggit.0002_auto_20150616_2121... OK

Provision with data
===================

You can load a small data sample for quick setup:

    $ memopol loaddata small_sample.json

Or actual data (takes a while)::

    $ bin/update_all

Run the development server
==========================

Run the development server::

    $ memopol runserver

    Performing system checks...

    System check identified no issues (0 silenced).
    December 09, 2015 - 21:26:47
    Django version 1.8.7, using settings 'memopol.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    [09/Dec/2015 21:26:48] "GET / HTTP/1.1" 200 13294

The website is running on ``http://127.0.0.1:8000/``.

Continue to :doc:`administration`.
