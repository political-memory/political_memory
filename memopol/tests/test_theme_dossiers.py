from .base import ThemeBaseTest


class ThemeDossiersTest(ThemeBaseTest):
    tab = 'dossiers'

    """
    Theme base queries plus
    - 1 for dossiers
    - 1 for related documents
    - 1 for related documents/chambers
    """
    queries = ThemeBaseTest.queries + 3

    def test_queries(self):
        self.do_query_test()

    def test_dossiers(self):
        self.selector_test('.dossier')
