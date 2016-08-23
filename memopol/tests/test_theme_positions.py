from .base import ThemeBaseTest


class ThemePositionsTest(ThemeBaseTest):
    tab = 'positions'

    """
    Theme base queries plus
    - 1 for positions
    """
    queries = ThemeBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_positions(self):
        self.selector_test('.position')
