import copy
import mock
import os
import pytest

from django.core.serializers.json import Deserializer
from django.core.management import call_command
from django.test import TestCase
from representatives_votes.contrib.parltrack import import_dossiers
from representatives_votes.contrib.parltrack import import_votes
from representatives_votes.models import Dossier, Proposal, Vote
import representatives
from representatives.models import Representative


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
        representatives.__path__[0]), 'fixtures', 'representatives_test.json'))
    call_command('loaddata', os.path.join(os.path.dirname(__file__),
        'dossiers_expected.json'))

    _test_import('votes', import_votes.main)


class DossierTest(TestCase):
    def setUp(self):
        for model in (Representative, Dossier, Proposal, Vote):
            model.objects.all().delete()

    def test_parltrack_import_single_dossier(self):
        call_command('loaddata', os.path.join(os.path.abspath(
            representatives.__path__[0]), 'fixtures',
            'representatives_test.json'))

        with self.assertNumQueries(22):
            _test_import('single', import_dossiers.import_single)

    def test_parltrack_sync_dossier(self):
        call_command('loaddata', os.path.join(os.path.abspath(
            representatives.__path__[0]), 'fixtures',
            'representatives_test.json'))
        call_command('loaddata', os.path.join(os.path.dirname(__file__),
            'sync_fixture.json'))

        reference = '2012/2002(INI)'
        mock_file = os.path.join(os.path.dirname(__file__),
            'parltrack_dossier_%s.json' % reference.replace('/', '-'))
        expected_url = '%s/dossier/%s?format=json' % (import_dossiers.BASEURL,
            reference)

        def callback(stream):
            import_dossiers.sync_dossier(reference)

        with mock.patch('urllib2.urlopen') as urlopen:
            with open(mock_file, 'r') as mock_stream:
                urlopen.return_value = mock_stream

                with self.assertNumQueries(8):
                    _test_import('sync', callback)

            urlopen.assert_called_with(expected_url)
