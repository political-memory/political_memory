from django import test

from responsediff.response import Response


class RepresentativeManagerTest(test.TestCase):
    fixtures = ['representatives_votes_test.json']

    def functional_test(self, queries, url):
        with self.assertNumQueries(queries):
            result = test.client.Client().get(url)
        Response.for_test(self).assertNoDiff(result)

    def test_dossiers(self):
        self.functional_test(1, '/api/dossiers/?format=json')

    def test_proposals(self):
        self.functional_test(1, '/api/proposals/?format=json')

    def test_votes(self):
        self.functional_test(1, '/api/votes/?format=json')
