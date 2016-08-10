from django import test
from responsediff.test import ResponseDiffTestMixin


class NavigationPaneTest(ResponseDiffTestMixin, test.TestCase):
    url = '/'

    def selector_test(self, selector):
        self.assertResponseDiffEmpty(test.Client().get(self.url), selector)

    def test_intro(self):
        self.selector_test('#intro')
