from .base import DossierBaseTest


class DossierProposalsTest(DossierBaseTest):
    tab = 'proposals'

    """
    Dossier base queries plus
    - 1 for proposals
    - 1 for related recommendations
    - 1 for related dossiers/documents
    - 1 for related dossiers/documents/chambers
    """
    queries = DossierBaseTest.queries + 4

    def test_queries(self):
        self.do_query_test()

    def test_proposals(self):
        self.selector_test('.proposal')
