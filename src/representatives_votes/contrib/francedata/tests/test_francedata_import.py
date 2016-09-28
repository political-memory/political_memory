import copy
import os
import pytest

from django.core.serializers.json import Deserializer
from django.core.management import call_command

from representatives.models import Representative
from representatives_votes.contrib.francedata import import_dossiers
from representatives_votes.contrib.francedata import import_scrutins
from representatives_votes.contrib.francedata import import_votes
from representatives_votes.models import Dossier, Proposal, Vote


def _get_testdata(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def _test_import(fixtures, scenario, callback):
    for model in (Representative, Dossier, Proposal, Vote):
        model.objects.all().delete()

    for fix in fixtures:
        call_command('loaddata', fix)

    inputfile = _get_testdata('%s_input.json' % scenario)
    expected = _get_testdata('%s_expected.json' % scenario)

    # Disable django auto fields
    exclude = ('id', '_state', 'created', 'updated', 'fingerprint')

    with open(inputfile, 'r') as f:
        callback(f)

    with open(expected, 'r') as f:
        for obj in Deserializer(f.read()):
            compare = copy.copy(obj.object.__dict__)

            for f in exclude:
                if f in compare:
                    compare.pop(f)

            type(obj.object).objects.get(**compare)


@pytest.mark.django_db
def test_francedata_import_dossiers():
    fixtures = []

    _test_import(fixtures, 'dossiers', import_dossiers.main)


@pytest.mark.django_db
def test_francedata_import_scrutins():
    fixtures = [
        _get_testdata('dossiers_expected.json')
    ]

    _test_import(fixtures, 'scrutins', import_scrutins.main)


@pytest.mark.django_db
def test_francedata_import_votes():
    fixtures = [
        _get_testdata('dossiers_expected.json'),
        _get_testdata('scrutins_expected.json'),
        _get_testdata('rep_fixture.json')
    ]

    _test_import(fixtures, 'votes', import_votes.main)
