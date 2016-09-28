from .base import BaseTest


class DossierListTest(BaseTest):
    url = '/dossiers/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.left_pane_queries + 6):
            """
            Left pane queries plus:
            - 1 for session key
            - 1 for dossier count (pagination)
            - 1 for dossiers
            - 1 for reverse relation on documents
            - 1 for reverse relation on document chambers
            - 1 for reverse relation on themes
            """
            self.client.get(self.url)

    def test_cards(self):
        self.selector_test('.dossier-card')

    def test_navbar_order_options(self):
        self.selector_test('#listheader #sort-menu li')

    def test_order_by_title_asc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort=title-asc' % self.url)

    def test_order_by_title_desc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort=title-desc' % self.url)

    def test_order_by_recommendations(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort=recommendations' % self.url)

    def test_order_by_proposals(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort=proposals' % self.url)
