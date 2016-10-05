import mock
import os

from django.core.management import call_command
from django.test import TestCase
from representatives_votes.contrib.parltrack import import_dossiers
from representatives_votes.contrib.parltrack import import_votes
from representatives_votes.models import Dossier, Proposal, Vote
import representatives
from representatives.models import Representative
from representatives.tests.base import TestBase


class ParltrackVotesTest(TestBase):
    def _test_import(self, scenario, callback):
        fixture = os.path.join(os.path.dirname(__file__),
                '%s_fixture.json' % scenario)
        expected = os.path.join(os.path.dirname(__file__),
                '%s_expected.json' % scenario)

        with open(fixture, 'r') as f:
            callback(f)

        self.assertObjectsFromFixture(expected)

    def test_parltrack_import_dossiers(self):
        self._test_import('dossiers', import_dossiers.main)

    def test_parltrack_import_votes(self):
        for model in (Representative, Dossier, Proposal, Vote):
            model.objects.all().delete()

        call_command('loaddata', os.path.join(os.path.abspath(
            representatives.__path__[0]), 'fixtures',
            'representatives_test.json'))
        call_command('loaddata', os.path.join(os.path.dirname(__file__),
            'dossiers_expected.json'))

        with mock.patch('representatives_votes.contrib.parltrack.import_votes'
                        '.Command.should_skip') as should_skip:
            should_skip.return_value = False
            self._test_import('votes', import_votes.main)

    def test_parltrack_import_single_dossier(self):
        call_command('loaddata', os.path.join(os.path.abspath(
            representatives.__path__[0]), 'fixtures',
            'representatives_test.json'))

        with self.assertNumQueries(22):
            self._test_import('single', import_dossiers.import_single)

    def test_parltrack_sync_dossier(self):
        for model in (Representative, Dossier, Proposal, Vote):
            model.objects.all().delete()

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
                    self._test_import('sync', callback)

            urlopen.assert_called_with(expected_url)
