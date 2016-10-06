import os

from representatives.models import Representative
from representatives.tests.base import TestBase
from representatives.contrib.parltrack import import_representatives


class ParltracRepresentativesTest(TestBase):
    def test_parltrack_import_representatives(self):
        fixture = os.path.join(os.path.dirname(__file__),
                'representatives_fixture.json')
        expected = os.path.join(os.path.dirname(__file__),
                'representatives_expected.json')

        with open(fixture, 'r') as f:
            import_representatives.main(f)

        self.assertObjectsFromFixture(expected)
        assert Representative.objects.count() == 2
