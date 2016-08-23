# coding: utf-8

from .theme_detail_base import ThemeDetailBase


class ThemeDetailProposals(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_proposals.html'

    def get_queryset(self):
        qs = super(ThemeDetailProposals, self).get_queryset()
        qs = qs.prefetch_related(
            'proposals__recommendation',
            'proposals__dossier__documents__chamber',
        )
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailProposals, self).get_context_data(**kwargs)

        c['tab'] = 'proposals'
        c['proposals'] = c['object'].proposals.all()

        return c
