from .base import ThemeBaseTest


class ThemeLinksTest(ThemeBaseTest):
    tab = 'links'

    """
    Theme base queries plus
    - 1 for links
    """
    queries = ThemeBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_links(self):
        self.selector_test('.link')
