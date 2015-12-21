# -*- coding: utf8 -*-
from django.test import TestCase

from .base import UrlGetTestMixin


class RepresentativeListTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/legislature/representative/'

    def test_num_queries(self):
        with self.assertNumQueries(3):
            """
            - A query on the session (for grid/list + pagination)
            - A count for pagination
            - One query for representative + score
            - One query for mandates (country + main_mandate)
            """
            self.client.get(self.url)
