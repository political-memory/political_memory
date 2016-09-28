from django import test

from responsediff.response import Response


class RepresentativeManagerTest(test.TestCase):
    fixtures = ['representatives_votes_test.json']

    def functional_test(self, queries, url):
        with self.assertNumQueries(queries):
            result = test.client.Client().get(
                url,
                HTTP_ACCEPT='application/json; indent=4',
            )
        Response.for_test(self).assertNoDiff(result)

    def test_dossier(self):
        # One for dossier
        # One for proposals
        # One for documents
        self.functional_test(3, '/api/dossiers/1/')

    def test_dossiers(self):
        self.functional_test(1, '/api/dossiers/')

    def test_proposal(self):
        # One for proposal and dossier + 1 for votes
        self.functional_test(2, '/api/proposals/1/')

    def test_proposals(self):
        self.functional_test(1, '/api/proposals/')

    def test_vote(self):
        self.functional_test(1, '/api/votes/1/')

    def test_votes(self):
        self.functional_test(1, '/api/votes/')
