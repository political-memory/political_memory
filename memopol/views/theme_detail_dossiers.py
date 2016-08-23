# coding: utf-8

from .theme_detail_base import ThemeDetailBase


class ThemeDetailDossiers(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_dossiers.html'

    def get_queryset(self):
        qs = super(ThemeDetailDossiers, self).get_queryset()
        qs = qs.prefetch_related('dossiers__documents__chamber')
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailDossiers, self).get_context_data(**kwargs)

        c['tab'] = 'dossiers'
        c['dossiers'] = c['object'].dossiers.all()

        return c
