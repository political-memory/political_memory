from .base import RepresentativeBaseTest


class RepresentativeMandatesTest(RepresentativeBaseTest):
    tab = 'mandates'

    """
    Representative queries plus
    - 1 for mandates
    """
    queries = RepresentativeBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_current_mandates(self):
        self.selector_test('.current-mandates .mandate')

    def test_past_mandates(self):
        self.selector_test('.past-mandates .mandate')
