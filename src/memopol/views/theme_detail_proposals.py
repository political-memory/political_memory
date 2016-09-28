# coding: utf-8

from django.db import models

from representatives_votes.models import Proposal

from .theme_detail_base import ThemeDetailBase


class ThemeDetailProposals(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_proposals.html'

    def get_queryset(self):
        qs = super(ThemeDetailProposals, self).get_queryset()
        qs = qs.prefetch_related(
            models.Prefetch(
                'proposals',
                Proposal.objects.select_related(
                    'recommendation', 'dossier'
                ).prefetch_related(
                    'dossier__documents__chamber'
                ).order_by('-datetime', 'title')
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailProposals, self).get_context_data(**kwargs)

        c['tab'] = 'proposals'
        c['proposals'] = c['object'].proposals.all()

        return c
