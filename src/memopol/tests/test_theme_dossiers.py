from .base import ThemeBaseTest


class ThemeDossiersTest(ThemeBaseTest):
    tab = 'dossiers'

    """
    Theme base queries plus
    - 1 for dossiers
    - 1 for reverse relation on documents
    - 1 for reverse relation on document chambers
    - 1 for reverse relation on themes
    """
    queries = ThemeBaseTest.queries + 4

    def test_queries(self):
        self.do_query_test()

    def test_dossiers(self):
        self.selector_test('.dossier')
