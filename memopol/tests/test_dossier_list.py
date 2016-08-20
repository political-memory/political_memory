from .base import BaseTest


class DossierListTest(BaseTest):
    url = '/votes/dossier/'

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
        self.selector_test('#listheader #orderby li, #listheader #orderdir li')

    def test_navbar_order_title_asc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort_by=title&sort_dir=asc' % self.url)

    def test_navbar_order_title_desc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort_by=title&sort_dir=desc' % self.url)

    def test_navbar_order_nb_proposals_asc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort_by=nb_proposals&sort_dir=asc' % self.url)

    def test_navbar_order_nb_proposals_desc(self):
        self.selector_test('.dossier-card h4',
                           '%s?sort_by=nb_proposals&sort_dir=desc' % self.url)

    def test_navbar_order_nb_recommendations_asc(self):
        self.selector_test('.dossier-card h4',
            '%s?sort_by=nb_recommendations&sort_dir=asc' % self.url)

    def test_navbar_order_nb_recommendations_desc(self):
        self.selector_test('.dossier-card h4',
            '%s?sort_by=nb_recommendations&sort_dir=desc' % self.url)
