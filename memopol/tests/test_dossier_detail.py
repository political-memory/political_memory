from .base import DossierBaseTest


class DossierDetailTest(DossierBaseTest):
    def test_queries(self):
        self.do_query_test()

    def test_name(self):
        return self.selector_test('#dossier-detail h1')

    def test_themes(self):
        return self.selector_test('#dossier-detail .tag')
