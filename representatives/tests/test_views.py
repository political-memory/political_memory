from django import test

from responsediff.response import Response

from representatives.models import Representative
from representatives.views import RepresentativeViewMixin


class RepresentativeManagerTest(test.TestCase):
    fixtures = ['representatives_test.json']

    def test_prefetch_profile(self):
        test = RepresentativeViewMixin()
        reps = test.prefetch_for_representative_country_and_main_mandate(
            Representative.objects.order_by('pk'))

        with self.assertNumQueries(2):
            # Cast to list to avoid [index] to cast a select with an offset
            # below !
            reps = [test.add_representative_country_and_main_mandate(r)
                    for r in reps]

            assert reps[0].country.code == 'AT'
            assert reps[0].main_mandate is None

            assert reps[1].country.code == 'SE'
            assert reps[1].main_mandate.pk == 15

    def functional_test(self, queries, url):
        with self.assertNumQueries(queries):
            result = test.client.Client().get(url)
        Response.for_test(self).assertNoDiff(result)

    def test_constituencies_api(self):
        self.functional_test(1, '/api/constituencies/?format=json')

    def test_groups_api(self):
        self.functional_test(1, '/api/groups/?format=json')

    def test_mandates_api(self):
        self.functional_test(1, '/api/mandates/?format=json')

    def test_representatives_api(self):
        """
        Queries:

        - representatives,
        - emails,
        - websites,
        - addresses,
        - phones,
        - mandates.
        """
        self.functional_test(6, '/api/representatives/?format=json')
