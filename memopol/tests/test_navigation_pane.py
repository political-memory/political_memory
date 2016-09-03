from .base import BaseTest


class NavigationPaneTest(BaseTest):
    url = '/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.left_pane_queries):
            self.client.get(self.url)

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
