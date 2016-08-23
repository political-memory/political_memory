from django import test
from responsediff.test import ResponseDiffTestMixin


class BaseTest(ResponseDiffTestMixin, test.TestCase):
    fixtures = ['data_sample.json']

    """
    Common queries
    - 1 for chambers
    - 1 for countries
    - 1 for parties
    - 1 for committees
    - 1 for delegations
    """
    left_pane_queries = 5

    def request_test(self, url=None):
        self.assertResponseDiffEmpty(self.client.get(url or self.url))

    def selector_test(self, selector, url=None):
        self.assertResponseDiffEmpty(self.client.get(url or self.url),
                                     selector)


class RepresentativeBaseTest(BaseTest):
    tab = 'none'
    base_url = '/legislature/representative/olivier-dussopt-1978-08-16/%s/'

    """
    Common queries plus:
    - 1 for chamber abbreviations (helper for chamber websites)
    - 1 for the representative
    - 1 for the main mandate
    - 1 for emails
    - 1 for social websites
    - 1 for chamber websites
    - 1 for other websites
    - 1 for addresses
    - 1 for phone numbers
    """
    queries = BaseTest.left_pane_queries + 9

    @property
    def url(self):
        return self.base_url % self.tab

    def do_query_test(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.queries):
            self.client.get(self.url)
