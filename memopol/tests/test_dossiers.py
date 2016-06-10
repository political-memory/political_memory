# -*- coding: utf8 -*-

from django.test import TestCase

from representatives_votes.models import Dossier

from .base import ResponseDiffMixin


class DossiersTest(ResponseDiffMixin, TestCase):
    fixtures = ['smaller_sample.json']

    def test_dossier_list(self):
        # session setup
        self.client.get('/votes/dossier/')

        # 1 query for dossier count
        # 1 query for dossiers
        # 1 query for proposals
        # 1 query for recommendations
        self.responsediff_test('/votes/dossier/', 4)

    def test_dossier_detail(self):
        # Get 1st dossier in dataset
        dossier = Dossier.objects.order_by('pk')[0]

        # session setup
        self.client.get('/votes/dossier/%s/' % dossier.pk)

        # 1 query for the dossier
        # 1 query for proposals
        # 1 query for recommendations
        self.responsediff_test('/votes/dossier/%s/' % dossier.pk, 3)
