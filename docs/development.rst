Local development tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warn:: I reverse-engineered this from the source code I inherited, I might
          not be doing the right way nor be able to defend all of technical
          decisions.

This tutorial drives through a local installation of the project for
development on Linux. It requires git, a fairly recent version of nodejs (see
:file:`.openshift/action_hooks/deploy` for a way to install it), python2 and
virtualenv.

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

And install the requirements::

    $ pip install -r requirements.txt
    Collecting django<1.9,>=1.8 (from -r requirements.txt (line 1))

    [output snipped for readability]

     Using cached Django-1.8.7-py2.py3-none-any.whl
      Running setup.py develop for django-representatives
      Running setup.py develop for django-representatives-votes
    Successfully installed amqp-1.4.8 anyjson-0.3.3 billiard-3.3.0.22 celery-3.1.19 django-1.8.7 django-adminplus-0.5 django-appconf-1.0.1 django-autocomplete-light-2.2.10 django-bootstrap3-6.2.2 django-celery-3.1.17 django-compressor-1.6 django-constance-1.1.1 django-datetime-widget-0.9.3 django-denorm-0.2.0 django-filter-0.11.0 django-picklefield-0.3.2 django-representatives django-representatives-votes django-taggit-0.17.5 django-uuidfield-0.5.0 djangorestframework-3.3.1 kombu-3.0.30 py-dateutil-2.2 pyprind-2.9.3 requests-2.8.1 slugify-0.0.1

Install NodeJS dependencies
===========================

We'll also need to install bower for the staticfiles::

    $ npm install bower
    memopol@3.0.0 /tmp/political_memory
    └── bower@1.7.0  extraneous

As well as all the requirements from :file:`package.json`::

    $ npm install
    memopol@3.0.0 /tmp/political_memory
    ├── bower@1.7.0  extraneous
    ├─┬ gulp@3.9.0

    [output snipped for readability]

    npm WARN In bower@1.7.0 replacing bundled version of configstore with configstore@0.3.2
    npm WARN In bower@1.7.0 replacing bundled version of latest-version with latest-version@1.0.1
    npm WARN In bower@1.7.0 replacing bundled version of update-notifier with update-notifier@0.3.2

Don't worry about the warnings, for they are non-critical (as all warnings).
Then, install the bower packages::

    $ node_modules/.bin/bower install
    bower bootstrap#~3.3.5          cached git://github.com/twbs/bootstrap.git#3.3.6
    bootstrap#3.3.6 static/libs/bootstrap
    └── jquery#2.1.4

    [output snipped for readability]

    jquery#2.1.4 static/libs/jquery

Build the static files with gulp::

    $ node_modules/gulp/bin/gulp.js less
    [22:26:42] Using gulpfile /tmp/political_memory/gulpfile.js
    [22:26:42] Starting 'less'...
    [22:26:44] Finished 'less' after 1.54 s

.. note:: The ``node_modules/gulp/bin/gulp.js watch`` command may be used to
          have gulp watching for changes and rebuilding static files
          automatically.

Activate ``DEBUG``
==================

``DEBUG`` is disabled by default, the development server won't run properly by
default thnen, to enable it export the ``DEBUG`` variable in the current
shell::

    $ export DEBUG=True

Database migrations
===================

Run database migrations, it'll use a file-based sqlite database by default::

    $ ./manage.py migrate
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

Run the development server
==========================

Run the development server::

    $ ./manage.py runserver

    Performing system checks...

    System check identified no issues (0 silenced).
    December 09, 2015 - 21:26:47
    Django version 1.8.7, using settings 'memopol.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    [09/Dec/2015 21:26:48] "GET / HTTP/1.1" 200 13294

The website is running on ``http://127.0.0.1:8000/``.

Provision with data
===================

To provision it with data (takes a while)::

    $ bin/update_all
