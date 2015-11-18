import pytest
import os
import copy

from django.core.serializers.json import Deserializer
from django.core.management import call_command
from representatives_votes.contrib.parltrack import import_dossiers
from representatives_votes.contrib.parltrack import import_votes
from representatives_votes.models import Dossier, Proposal, Vote
from representatives.models import Representative
from representatives.contrib import parltrack


def _test_import(scenario, callback):
    fixture = os.path.join(os.path.dirname(__file__),
            '%s_fixture.json' % scenario)
    expected = os.path.join(os.path.dirname(__file__),
            '%s_expected.json' % scenario)

    # Disable django auto fields
    exclude = ('id', '_state', 'created', 'updated')

    with open(fixture, 'r') as f:
        callback(f)

    with open(expected, 'r') as f:
        for obj in Deserializer(f.read()):
            compare = copy.copy(obj.object.__dict__)

            for f in exclude:
                if f in compare:
                    compare.pop(f)

            type(obj.object).objects.get(**compare)


@pytest.mark.django_db
def test_parltrack_import_dossiers():
    _test_import('dossiers', import_dossiers.main)


@pytest.mark.django_db
def test_parltrack_import_votes():
    for model in (Representative, Dossier, Proposal, Vote):
        model.objects.all().delete()

    call_command('loaddata', os.path.join(os.path.abspath(
        parltrack.__path__[0]), 'tests', 'representatives_expected.json'))
    call_command('loaddata', os.path.join(os.path.dirname(__file__),
        'dossiers_expected.json'))

    _test_import('votes', import_votes.main)
