from .base import DossierBaseTest


class DossierRecommendationsTest(DossierBaseTest):
    tab = 'recommendations'

    """
    Dossier base queries plus
    - 1 for proposals and related recommendation
    - 1 for related themes
    """
    queries = DossierBaseTest.queries + 2

    def test_queries(self):
        self.do_query_test()

    def test_proposals(self):
        self.selector_test('.proposal')
