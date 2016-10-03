Hacker guide
~~~~~~~~~~~~

See a `hacking demo on the Memopol project in some epic
slides
<https://slides.com/jamespic/cd-devops/fullscreen#/>`_.

Read about it in `Continuous Delivery and DevOps
quickstart
<https://www.packtpub.com/application-development/continuous-delivery-and-devops-%E2%80%93-quickstart-guide-second-edition)>`_,
and I bet you'll order a paperback edition for reference !

Testing
=======

Use the ``tox -l`` command to list tests::

    $ pip install tox
    $ cd political_memory/
    $ tox -l

Use the ``tox -e`` command to execute a particular test suite::

    $ tox -e py27

And use the ``tox`` command without argument to execute all test suites,
exactly like in CI.

Adding random recommendations
=============================

::

    $ memopol shell
    In [1]: from representatives_votes.models import Proposal
    In [2]: from votes.models import Recommendation
    In [3]: import random

    In [4]: for p in Proposal.objects.all(): Recommendation.objects.create(proposal=p, recommendation='for', weight=random.randint(1,10))


Creating test fixtures
======================

The largest test fixtures are, the longer it takes to load them, the longer the
test run is.

To create test fixtures for representatives_positions, insert some Position
objects, and reduce the database with::

    memopol remove_representatives_without_position
    memopol remove_groups_without_mandate
    memopol remove_countries_without_group

For representatives_recommendations::

    memopol remove_proposals_without_recommendation
    memopol remove_dossiers_without_proposal
    memopol remove_representatives_without_vote
    memopol remove_groups_without_mandate
    memopol remove_countries_without_group
