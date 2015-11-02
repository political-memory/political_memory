Deployment on OpenShift
~~~~~~~~~~~~~~~~~~~~~~~

OpenShift is an Open-Source Platform-as-a-Service software by Red Hat. It is
also available in its hosted version known as "OpenShift Online" and the first
three websites ("gears") are free.

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

Create an app on OpenShift
==========================

To deploy the website, use a command like::

    $ rhc app-create \
        python-2.7 \
        "http://cartreflect-claytondev.rhcloud.com/reflect?github=smarterclayton/openshift-redis-cart" \
        cron-1.4 \
        postgresql-9.2 \
        -a yourappname \
        -e OPENSHIFT_PYTHON_WSGI_APPLICATION=memopol/wsgi.py \
        --from-code https://github.com/political-memory/political_memory.git

This should create an app on openshift. Other commands would deploy it at once
but in this tutorial we're going to see how to manage it partly manually for
development.

Add the git remote created by OpenShift
=======================================

Add the git remote openshift created for you, you can see it with
``rhc app-show``, ie.::

    $ rhc app-show -a yourappname
    [snip]
    Git URL:         ssh://569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com/~/git/yourappname.git/
    Initial Git URL: https://github.com/political-memory/political_memory.git
    SSH:             569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com
    [snip]

    $ git remote add oo_yourappname ssh://569f5cf500045f6a1839a0a4@yourappname-yourdomain.rhcloud.com/~/git/yourappname.git/

Activate OpenShift's git post-recieve hook
==========================================

Activate OpenShift's post-receive hook on your branch::

    $ rhc app-configure -a yourappname --deployment-branch yourbranch

Deploy your branch
==================

OpenShift will deploy when it receives commits on the deployment branch, to
deploy just do::

    $ git push oo_yourappname yourbranch

If something goes wrong and you want to retry, use the ``rhc app-deploy``
command, ie::

    $ rhc app-deploy yourbranch -a yourappname

Data provisionning
==================

To fill up the representatives database table, either wait for the cron script
to be executed, either do it manually::

    $ rhc ssh -a yourappname 'cd app-root/repo/ && bin/update_all'

OpenShift is fun, login with ssh and look around if you're curious, you'll be
able to recreate your app without much effort if you break it anyway.
