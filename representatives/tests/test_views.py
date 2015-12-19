from django.test import TestCase

from representatives.models import Representative
from representatives.views import RepresentativeViewMixin


class RepresentativeManagerTest(TestCase):
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
