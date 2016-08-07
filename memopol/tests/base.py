import re
import os.path

from django.test import Client

from responsediff.response import Response


class UrlGetTestMixin(object):
    url = None

    def setUp(self):
        self.client = Client()

        if not hasattr(type(self), 'response'):
            # Do it once and for all, note that this also caches content types
            # so the contenttype query used by taggit won't be counted in
            # test_num_queries.
            self.__class__.response = self.client.get(self.url)
        self.response = self.__class__.response

    def assertHtmlInResult(self, expected):
        compare = re.sub('[\s"\']', '', expected)
        result = re.sub('[\s"\']', '', self.response.content)
        self.assertIn(compare, result)

    def assertExpectedHtmlInResult(self):
        """
        For test_votes_display, it is:
        /positions/tests/test_representatives_detail_test_votes_display_expected.html
        """
        expected = os.path.join(
            os.path.dirname(__file__),
            type(self).__name__,
            '%s.html' % self._testMethodName
        )

        with open(expected, 'r') as f:
            self.assertHtmlInResult(f.read())


class ResponseDiffMixin(object):

    def responsediff_test(self, url, numQueries):
        self.client.cookies['csrftoken'] = 'csrftoken'
        with self.assertNumQueries(numQueries):
            response = self.client.get(url)

        expected = Response.for_test(self)
        expected.assertNoDiff(response)
