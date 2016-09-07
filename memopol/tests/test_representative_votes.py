from .base import RepresentativeBaseTest


class RepresentativeVotesTest(RepresentativeBaseTest):
    tab = 'votes'

    """
    - One for votes
    - One for dossier scores
    - Two for dossier themes (?? should be one according to the queryset !)
    """
    queries = RepresentativeBaseTest.queries + 4

    def test_queries(self):
        self.do_query_test()

    def test_dossiers(self):
        self.selector_test('#accordion-dossier h4 a')

    def test_votes(self):
        self.selector_test('#accordion-dossier tr')
