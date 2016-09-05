# coding: utf-8

from .theme_detail_base import ThemeDetailBase


class ThemeDetailPositions(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_positions.html'

    def get_queryset(self):
        qs = super(ThemeDetailPositions, self).get_queryset()
        qs = qs.prefetch_related('positions__representative',
                                 'positions__positionscore')
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailPositions, self).get_context_data(**kwargs)

        c['tab'] = 'positions'
        c['positions'] = c['object'].positions.all()

        return c
