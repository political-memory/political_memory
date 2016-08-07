# coding: utf-8

from core.views import PaginationMixin

from django.views import generic

from memopol_themes.models import Theme

from ..filters import ThemeFilter


class ThemeList(PaginationMixin, generic.ListView):

    current_filter = None
    queryset = Theme.objects.all()

    def theme_filter(self, qs):
        f = ThemeFilter(self.request.GET, queryset=qs)
        self.current_filter = f
        return f.qs

    def get_queryset(self):
        qs = super(ThemeList, self).get_queryset()
        qs = self.theme_filter(qs)
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeList, self).get_context_data(**kwargs)
        c['filter'] = self.current_filter
        return c
