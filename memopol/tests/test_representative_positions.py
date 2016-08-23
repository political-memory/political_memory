from .base import RepresentativeBaseTest


class RepresentativePositionsTest(RepresentativeBaseTest):
    tab = 'positions'

    """
    - One for positions
    """
    queries = RepresentativeBaseTest.queries + 1

    def test_queries(self):
        self.do_query_test()

    def test_position_buttons(self):
        self.selector_test('.position-button')

    def test_position_details(self):
        self.selector_test('.position-details')
