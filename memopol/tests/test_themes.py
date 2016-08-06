# -*- coding: utf8 -*-

from django.test import TestCase

from memopol_themes.models import Theme

from .base import ResponseDiffMixin


class ThemesTest(ResponseDiffMixin, TestCase):
    fixtures = ['smaller_sample.json']

    def test_theme_list(self):
        # session setup
        self.client.get('/theme/')

        # 1 query for theme count
        # 1 query for themes
        self.responsediff_test('/theme/', 2)

    def test_theme_search(self):
        # session setup
        self.client.get('/theme/')

        # 1 query for theme count
        # 1 query for themes
        q = 'acta'
        self.responsediff_test('/theme/?search=%s' % q, 2)

    def test_theme_search_noresults(self):
        # session setup
        self.client.get('/theme/')

        # 1 query for theme count
        # nothing else since count = 0
        q = 'no-theme-will-have-that-title-ever'
        self.responsediff_test('/theme/?search=%s' % q, 1)

    def test_theme_detail(self):
        # Get 1st theme in dataset
        theme = Theme.objects.order_by('pk')[0]

        # session setup
        self.client.get('/theme/%s/' % theme.pk)

        # 1 query for the theme
        # 1 query for links
        # 1 query for dossiers
        # 1 query for dossier documents
        # 1 query for dossier document chambers
        # 1 query for proposals
        # 1 query for proposals dossiers
        # 1 query for proposals dossier documents
        # 1 query for proposals dossier document chambers
        # 1 query for positions
        # 1 query for position representativs
        self.responsediff_test('/theme/%s/' % theme.slug, 11)
