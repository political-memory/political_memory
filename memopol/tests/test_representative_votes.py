from .base import RepresentativeBaseTest


class RepresentativeVotesTest(RepresentativeBaseTest):
    tab = 'votes'

    """
    - One for votes
    - One for dossier scores
    """
    queries = RepresentativeBaseTest.queries + 2

    def test_queries(self):
        self.do_query_test()

    def test_dossiers(self):
        self.selector_test('#accordion-dossier h4 a')

    def test_votes(self):
        self.selector_test('#accordion-dossier tr')
