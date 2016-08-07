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

    def functional_test(self, page, paginate_by, active_only, display,
                        search=''):
        url = '%s?page=%s&search=%s' % (self.url, page, search)

        # Cancel out one-time queries (session)
        self.client.get('%s&paginate_by=%s&display=%s&active_only=%s' %
            (url, paginate_by, display, active_only))

        with self.assertNumQueries(5):
            """
            - A count for pagination
            - One query for chambers (filters)
            - One query for countries (filters)
            - One query for representative + score
            - One query for mandates (including country + main_mandate)
            """
            self.response = self.client.get(url)

        expected = Response.for_test(self)
        expected.assertNoDiff(self.response)

    def filter_test(self, num_queries, search='', country='', chamber='',
                    group=''):
        url = '%s?search=%s&country=%s&chamber=%s&group=%s' % (self.url,
            search, country, chamber, group)

        # Cancel out one-time queries (session)
        self.client.get('%s&paginate_by=12&active_only=1' % url)

        with self.assertNumQueries(num_queries):
            self.response = self.client.get(url)

        expected = Response.for_test(self)
        expected.assertNoDiff(self.response)

    def sorting_test(self, num_queries, field='', dir=''):
        url = '%s?sort_by=%s&sort_dir=%s' % (self.url, field, dir)

        # Cancel out one-time queries (session)
        self.client.get('%s&paginate_by=12&active_only=1' % url)

        with self.assertNumQueries(num_queries):
            self.response = self.client.get(self.url)

        expected = Response.for_test(self)
        expected.assertNoDiff(self.response)

    def test_page1_paginateby12_active_displaylist(self):
        self.functional_test(1, 12, 1, 'list')

    def test_page1_paginateby12_all_displaylist(self):
        self.functional_test(1, 12, 0, 'list')

    def test_page1_paginateby24_active_displaygrid(self):
        self.functional_test(1, 24, 1, 'grid')

    def test_page1_paginateby24_all_displaygrid(self):
        self.functional_test(1, 24, 0, 'grid')

    def test_page2_paginateby24_displaylist(self):
        self.functional_test(2, 24, 1, 'list')

    def test_page1_paginateby12_displaylist_searchjoly(self):
        self.functional_test(1, 12, 1, 'list', 'joly')

    def test_page2_paginateby12_displaylist(self):
        self.functional_test(2, 12, 1, 'list')

    def test_filter_search(self):
        """
        - A count for pagination
        - One query for representative + score
        - One query for mandates (including country + main_mandate)
        - One query for chambers (filters)
        - One query for countries (filters)
        """
        self.filter_test(5, 'am')

    def test_filter_country(self):
        """
        5 same queries as test_filter_search plus:
        - One query for the country
        """
        self.filter_test(6, '', 110)

    def test_filter_chamber(self):
        """
        5 same queries as test_filter_search plus:
        - One query for the chamber
        """
        self.filter_test(6, '', '', 1)

    def test_filter_group(self):
        """
        5 same queries as test_filter_search plus:
        - One query for the group
        - One query to display the group name (DAL select2 widget)
        """
        self.filter_test(7, '', '', '', 17)

    def test_filter_multiple(self):
        """
        5 same queries as test_filter_search plus:
        - One query for the country
        - One query for the chamber
        - One query for the group
        - One query to display the group name (DAL select2 widget)
        """
        self.filter_test(9, 'e', 110, 1, 17)

    def test_filter_notfound(self):
        """
        Same queries as test_filter_search minus those two :
        - One query for representative + score
        - One query for mandates (including country + main_mandate)
        (as the first count query returns 0)
        """
        self.filter_test(3, 'non-existing-rep-name')

    def test_sorting(self):
        """
        - A count for pagination
        - One query for chambers (filters)
        - One query for countries (filters)
        - One query for representative + score
        - One query for mandates (including country + main_mandate)
        """
        self.sorting_test(5, 'score', 'desc')
