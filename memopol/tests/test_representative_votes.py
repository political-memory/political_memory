from .base import RepresentativeBaseTest


class RepresentativeVotesTest(RepresentativeBaseTest):
    tab = 'votes'

    """
    - One for votes
    """
    queries = RepresentativeBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_dossiers(self):
        self.selector_test('#accordion-dossier h4 a')

    def test_votes(self):
        self.selector_test('#accordion-dossier tr')
