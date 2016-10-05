import os

from representatives.models import Representative
from representatives.tests.base import TestBase
from representatives.contrib.francedata import import_representatives


class FranceDataRepresentativesTest(TestBase):
    def test_francedata_import_representatives(self):
        inputjson = os.path.join(os.path.dirname(__file__),
                'representatives_input.json')
        expected = os.path.join(os.path.dirname(__file__),
                'representatives_expected.json')

        with open(inputjson, 'r') as f:
            import_representatives.main(f)

        self.assertObjectsFromFixture(expected)
        assert Representative.objects.count() == 2
