from django.test import TestCase

from .base import UrlGetTestMixin


class DossiersListTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/votes/dossier/'

    def test_num_queries(self):
        """
        1) fetch the total dossiers count for the paginator
        2) fetch the dossiers in the current page
        """
        # Cancel out one-time queries (session)
        self.client.get(self.url)

        with self.assertNumQueries(2):
            resp = self.client.get(self.url)

    def test_page_title(self):
        self.assertHtmlInResult('<p class="lead text-center">1 dossier.</p>')

    def test_dossier_title(self):
        self.assertHtmlInResult('<h4 class="text-center">Resolution on the Anti-Counterfeiting Trade Agreement (ACTA)</h4>')

    def test_dossier_age(self):
        self.assertHtmlInResult('<p class="text-center">Last updated Dec. 27, 2015</p>')

    def test_dossier_votes(self):
        self.assertHtmlInResult('<span class="badge">106</span>')
