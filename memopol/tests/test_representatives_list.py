# -*- coding: utf8 -*-
from django.test import TestCase

from responsediff.response import Response

from .base import UrlGetTestMixin


class RepresentativeListTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/legislature/representative/'

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
