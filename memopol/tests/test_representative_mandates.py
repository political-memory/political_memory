from .base import RepresentativeBaseTest


class RepresentativeMandatesTest(RepresentativeBaseTest):
    tab = 'mandates'

    """
    No additional queries (mandates already prefetched for rep header box)
    """
    queries = RepresentativeBaseTest.queries

    def test_queries(self):
        self.do_query_test()

    def test_mandates(self):
        self.selector_test('.mandate')
