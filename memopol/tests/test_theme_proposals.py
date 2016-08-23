from .base import ThemeBaseTest


class ThemeProposalsTest(ThemeBaseTest):
    tab = 'proposals'

    """
    Theme base queries plus
    - 1 for proposals
    - 1 for related recommendations
    - 1 for related dossiers
    - 1 for related dossiers/documents
    - 1 for related dossiers/documents/chambers
    """
    queries = ThemeBaseTest.queries + 5

    def test_queries(self):
        self.do_query_test()

    def test_proposals(self):
        self.selector_test('.proposal')
