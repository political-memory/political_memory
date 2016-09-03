from .base import DossierBaseTest


class DossierDocumentsTest(DossierBaseTest):
    tab = 'documents'

    """
    Dossier base queries plus
    - 1 for documents
    - 1 for related chambers
    """
    queries = DossierBaseTest.queries + 2

    def test_queries(self):
        self.do_query_test()

    def test_proposals(self):
        self.selector_test('.document')
