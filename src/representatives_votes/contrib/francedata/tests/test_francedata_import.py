import os

from django.core.management import call_command

from representatives.models import Representative
from representatives.tests.base import TestBase
from representatives_votes.contrib.francedata import import_dossiers
from representatives_votes.contrib.francedata import import_scrutins
from representatives_votes.contrib.francedata import import_votes
from representatives_votes.models import Dossier, Proposal, Vote


def _get_testdata(filename):
    return os.path.join(os.path.dirname(__file__), filename)


class FranceDataVotesTest(TestBase):
    def _test_import(self, fixtures, scenario, callback):
        for model in (Representative, Dossier, Proposal, Vote):
            model.objects.all().delete()

        for fix in fixtures:
            call_command('loaddata', fix)

        inputfile = _get_testdata('%s_input.json' % scenario)
        expected = _get_testdata('%s_expected.json' % scenario)

        with open(inputfile, 'r') as f:
            callback(f)

        self.assertObjectsFromFixture(expected)

    def test_francedata_import_dossiers(self):
        fixtures = []

        self._test_import(fixtures, 'dossiers', import_dossiers.main)

    def test_francedata_import_scrutins(self):
        fixtures = [
            _get_testdata('dossiers_expected.json')
        ]

        self._test_import(fixtures, 'scrutins', import_scrutins.main)

    def test_francedata_import_votes(self):
        fixtures = [
            _get_testdata('dossiers_expected.json'),
            _get_testdata('scrutins_expected.json'),
            _get_testdata('rep_fixture.json')
        ]

        self._test_import(fixtures, 'votes', import_votes.main)
