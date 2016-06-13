# -*- coding: utf8 -*-

from django.test import TestCase

from .base import ResponseDiffMixin


class GroupListTest(ResponseDiffMixin, TestCase):
    fixtures = ['smaller_sample.json']

    def group_test(self, kind, active_only, numQueries):
        url = '/legislature/group/%s/' % kind

        # setup session variables
        self.client.get('%s?active_only=%s' % (url, active_only))

        self.responsediff_test(url, numQueries)

    def test_chambers(self):
        # 1 query for chambers
        # 1 query for pagination
        self.group_test('chamber', 1, 2)

    def test_country(self):
        # 1 query for countries
        # 1 query for pagination
        self.group_test('country', 1, 2)

    def test_active_parties(self):
        # 1 query for political groups
        # 1 query for pagination
        self.group_test('group', 1, 2)

    def test_all_parties(self):
        # 1 query for political groups
        # 1 query for pagination
        self.group_test('group', 0, 2)

    def test_active_delegations(self):
        # 1 query for delegations
        # 1 query for pagination
        self.group_test('delegation', 1, 2)

    def test_all_delegations(self):
        # 1 query for delegations
        # 1 query for pagination
        self.group_test('delegation', 0, 2)

    def test_active_committees(self):
        # 1 query for committees
        # 1 query for pagination
        self.group_test('committee', 1, 2)

    def test_all_committees(self):
        # 1 query for committees
        # 1 query for pagination
        self.group_test('committee', 0, 2)
