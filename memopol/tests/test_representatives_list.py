# -*- coding: utf8 -*-

from django.test import TestCase

from responsediff.response import Response


from .base import UrlGetTestMixin
from representatives.models import Representative
from ..views.representative_mixin import RepresentativeViewMixin


class RepresentativeListTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/legislature/representative/'

    def test_prefetch_profile(self):
        test = RepresentativeViewMixin()
        reps = test.prefetch_for_representative_country_and_main_mandate(
            Representative.objects.order_by('pk'))

        with self.assertNumQueries(2):
            # Cast to list to avoid [index] to cast a select with an offset
            # below !
            reps = [test.add_representative_country_and_main_mandate(r)
                    for r in reps]

            assert reps[0].country.code == 'GB'
            assert reps[0].main_mandate.pk == 3318

            assert reps[1].country.code == 'FI'
            assert reps[1].main_mandate.pk == 5545

    def functional_test(self, page, paginate_by, display, search=''):
        url = '%s?page=%s&search=%s' % (self.url, page, search)

        # Cancel out one-time queries (session)
        self.client.get('%s&paginate_by=%s&display=%s' %
            (url, paginate_by, display))

        with self.assertNumQueries(3):
            """
            - A count for pagination
            - One query for representative + score
            - One query for mandates (including country + main_mandate)
            """
            self.response = self.client.get(url)

        expected = Response.for_test(self)
        expected.assertNoDiff(self.response)

    def test_page1_paginateby12_displaylist(self):
        self.functional_test(1, 12, 'list')

    def test_page1_paginateby24_displaygrid(self):
        self.functional_test(1, 24, 'grid')

    def test_page2_paginateby24_displaylist(self):
        self.functional_test(2, 24, 'list')

    def test_page1_paginateby12_displaylist_searchjoly(self):
        self.functional_test(1, 12, 'list', 'joly')

    def test_page2_paginateby12_displaylist(self):
        self.functional_test(2, 12, 'list')
