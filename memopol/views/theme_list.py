# coding: utf-8

from core.views import PaginationMixin, SortMixin

from django.db.models import Count
from django.views import generic

from memopol_themes.models import Theme

from ..filters import ThemeFilter

from representatives_positions.views import PositionFormMixin


class ThemeList(PaginationMixin, SortMixin, PositionFormMixin,
                generic.ListView):

    current_filter = None
    queryset = Theme.objects.all().annotate(
        nb_links=Count('links', distinct=True),
        nb_dossiers=Count('dossiers', distinct=True),
        nb_proposals=Count('proposals', distinct=True),
        nb_positions=Count('positions', distinct=True)
    )

    sort_fields = {
        'name': 'name',
    }
    sort_default_field = 'name'
    sort_session_prefix = 'theme_list'

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
        c['view'] = 'theme_list'
        return c
