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
