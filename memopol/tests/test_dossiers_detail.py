from django.test import TestCase

from .base import UrlGetTestMixin


class DossierDetailTest(UrlGetTestMixin, TestCase):
    fixtures = ['smaller_sample.json']
    url = '/votes/dossier/28147/'

    def test_num_queries(self):
        """
        1) fetch the dossier
        2) fetch the proposals
        3) fetch the representatives
        4) prefetch the votes
        """

        # Ensure one-time cached queries occur before the actual test
        self.client.get(self.url)

        with self.assertNumQueries(4):
            self.client.get(self.url)

    def test_title_display(self):
        self.assertHtmlInResult("<h1 class='text-center'>Dossier Resolution on the Anti-Counterfeiting Trade Agreement (ACTA)</h1>")

    def test_date_display(self):
        self.assertHtmlInResult("<p class='lead text-center'>Last updated Dec. 27, 2015</p>")

    def test_description_display(self):
        self.assertExpectedHtmlInResult()

    def test_votes_display(self):
        self.assertExpectedHtmlInResult()
