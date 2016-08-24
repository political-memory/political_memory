from .base import DossierBaseTest


class DossierRecommendationsTest(DossierBaseTest):
    tab = 'recommendations'

    """
    Dossier base queries plus
    - 1 for proposals and related recommendation
    """
    queries = DossierBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_proposals(self):
        self.selector_test('.proposal')
