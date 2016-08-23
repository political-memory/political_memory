from .base import RepresentativeBaseTest


class RepresentativeDetailTest(RepresentativeBaseTest):
    def test_queries(self):
        self.do_query_test()

    def test_photo(self):
        return self.selector_test('#representative-photo')

    def test_name(self):
        return self.selector_test('#representative-detail h1')

    def test_details(self):
        return self.selector_test('#representative-detail dd')
