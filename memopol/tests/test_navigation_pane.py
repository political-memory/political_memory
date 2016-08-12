from django import test
from responsediff.test import ResponseDiffTestMixin


class NavigationPaneTest(ResponseDiffTestMixin, test.TestCase):
    url = '/'
    fixtures = ['smaller_sample.json']

    """
    Common queries
    - One for chambers
    - One for countries
    - One for parties
    - One for committees
    - One for delegations
    """
    queries = 5

    def selector_test(self, selector):
        self.assertResponseDiffEmpty(test.Client().get(self.url), selector)

    def test_queries(self):
        with self.assertNumQueries(self.queries):
            test.Client().get(self.url)

    def test_rep_search_chambers(self):
        self.selector_test('#form-rep #chamber-rep option')

    def test_rep_search_countries(self):
        self.selector_test('#form-rep #country option')

    def test_rep_search_parties(self):
        self.selector_test('#form-rep #party option')

    def test_rep_search_committee(self):
        self.selector_test('#form-rep #committee option')

    def test_rep_search_delegation(self):
        self.selector_test('#form-rep #delegation option')

    def test_dossier_search_chambers(self):
        self.selector_test('#form-dossier #chamber-dossier option')
