# -*- coding: utf-8 -*-
from django.test import TestCase

from .base import UrlGetTestMixin


class RepresentativeDetailTest(UrlGetTestMixin, TestCase):
    fixtures = ['one_representative']
    url = '/legislature/representative/mary-honeyball-1952-11-12/'

    def test_num_queries(self):
        # Ensure one-time cached queries occur before the actual test
        self.client.get(self.url)

        with self.assertNumQueries(11):
            """
            - One query for chambers
            - One query for the rep details and foreign key (profile)
            - One query for reverse relation on phones
            - One query for reverse relation on addresses
            - One query for reverse relation on emails
            - Three queries for reverse relation on websites (parliament,
              social and other)
            - One query for reverse relation on votes
            - One query for reverse relation on mandates
            - One query for reverse relation positions
            """
            self.client.get(self.url)

    def test_name_display(self):
        # When HAMLPY_ATTR_WRAPPER works, use double quotes in HTML attrs !
        self.assertHtmlInResult("<h1 class='text-left'>Mary HONEYBALL</h1>")

    def test_score_display(self):
        self.assertExpectedHtmlInResult()

    def test_country_display(self):
        self.assertHtmlInResult(
            '<span class="flag-icon flag-icon-gb"></span> United Kingdom')

    def test_current_mandate_display(self):
        expected = ''.join((
            "<a href='/legislature/representative/group/European%20Parliament/Group%20of%20the%20Progressive%20Alliance%20of%20Socialists%20and%20Democrats%20in%20the%20European%20Parliament/'>",  # noqa
            "<span class='group-icon' style='background-image: url(/static/collected/images/group-ep-sd.png)'></span>",  # noqa
            "Member of Group of the Progressive Alliance of Socialists and Democrats in the European Parliament",  # noqa
            "</a>",
        ))
        self.assertHtmlInResult(expected)

    def test_biography_display(self):
        self.assertHtmlInResult('Born in Weymouth the 12/11/1952 (F)')

    def test_votes_display(self):
        self.assertExpectedHtmlInResult()

    def test_mandates_display(self):
        self.assertExpectedHtmlInResult()

    def test_positions_display(self):
        self.assertExpectedHtmlInResult()
