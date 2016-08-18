from .base import BaseTest


class RepresentativeListTest(BaseTest):
    url = '/legislature/representative/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.left_pane_queries + 4):
            """
            Left pane queries plus:
            - 1 for session key
            - 1 for representative count (pagination)
            - 1 for representatives
            - 1 for reverse relation on country
            """
            self.client.get(self.url)

    def test_cards(self):
        self.selector_test('.representative-card')

    def test_search_no_results(self):
        self.selector_test('.representative-card h4',
                           '%s?search=non-existing' % self.url)

    def test_search_by_name(self):
        self.selector_test('.representative-card h4',
                           '%s?search=ma' % self.url)

    def test_search_by_chamber(self):
        self.selector_test('.representative-card h4',
                           '%s?chamber=1' % self.url)

    def test_search_by_country(self):
        self.selector_test('.representative-card h4',
                           '%s?country=145' % self.url)

    def test_search_by_party(self):
        self.selector_test('.representative-card h4',
                           '%s?party=21' % self.url)

    def test_search_by_committee(self):
        self.selector_test('.representative-card h4',
                           '%s?committee=7' % self.url)

    def test_search_by_delegation(self):
        self.selector_test('.representative-card h4',
                           '%s?delegation=95' % self.url)
