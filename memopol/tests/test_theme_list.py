from .base import BaseTest


class ThemeListTest(BaseTest):
    url = '/theme/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.left_pane_queries + 3):
            """
            Left pane queries plus:
            - 1 for session key
            - 1 for theme count (pagination)
            - 1 for themes
            """
            self.client.get(self.url)

    def test_cards(self):
        self.selector_test('.theme-card')

    def test_navbar_order_options(self):
        self.selector_test('#listheader #orderby li, #listheader #orderdir li')

    def test_navbar_order_name_asc(self):
        self.selector_test('.theme-card h4',
                           '%s?sort_by=name&sort_dir=asc' % self.url)

    def test_navbar_order_name_desc(self):
        self.selector_test('.theme-card h4',
                           '%s?sort_by=name&sort_dir=desc' % self.url)
