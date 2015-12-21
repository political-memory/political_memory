Hacker guide
~~~~~~~~~~~~

Adding random recommendations
=============================

::

    $ ./manage.py shell
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

    ./manage.py remove_representatives_without_position
    ./manage.py remove_groups_without_mandate
    ./manage.py remove_countries_without_group

For representatives_recommendations::

    ./manage.py remove_proposals_without_recommendation
    ./manage.py remove_dossiers_without_proposal
    ./manage.py remove_representatives_without_vote
    ./manage.py remove_groups_without_mandate
    ./manage.py remove_countries_without_group
