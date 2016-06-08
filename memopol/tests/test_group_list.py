# -*- coding: utf8 -*-

from django.test import TestCase

from responsediff.response import Response


class GroupListTest(TestCase):
    fixtures = ['smaller_sample.json']

    def group_test(self, kind, numQueries):
        url = '/legislature/group/%s/' % kind

        # Setup session variables
        self.client.get(url)

        with self.assertNumQueries(numQueries):
            response = self.client.get(url)

        expected = Response.for_test(self)
        expected.assertNoDiff(response)

    def test_chambers(self):
        # 1 query for chambers
        self.group_test('chamber', 1)

    def test_country(self):
        # 1 query for countries
        self.group_test('country', 1)

    def test_parties(self):
        # 1 query for political groups
        self.group_test('group', 1)

    def test_delegations(self):
        # 1 query for delegations
        self.group_test('delegation', 1)

    def test_committees(self):
        # 1 query for committees
        self.group_test('committee', 1)
