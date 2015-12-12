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

