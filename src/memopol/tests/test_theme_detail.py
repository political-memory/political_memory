from .base import ThemeBaseTest


class ThemeDetailTest(ThemeBaseTest):
    def test_queries(self):
        self.do_query_test()

    def test_name(self):
        return self.selector_test('#theme-detail h1')

    def test_description(self):
        return self.selector_test('#theme-detail #description')
