# coding: utf-8

from .theme_detail_base import ThemeDetailBase


class ThemeDetailLinks(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_links.html'

    def get_queryset(self):
        qs = super(ThemeDetailLinks, self).get_queryset()
        qs = qs.prefetch_related('links')
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailLinks, self).get_context_data(**kwargs)

        c['tab'] = 'links'
        c['links'] = c['object'].links.all()

        return c
