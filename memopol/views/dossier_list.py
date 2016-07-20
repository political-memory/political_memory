# coding: utf-8

from core.views import PaginationMixin, SortMixin

from django.db.models import Count
from django.views import generic

from representatives_votes.models import Dossier

from ..filters import DossierFilter


class DossierList(PaginationMixin, SortMixin, generic.ListView):

    current_filter = None
    queryset = Dossier.objects.prefetch_related(
        'proposals',
        'proposals__recommendation',
        'documents',
        'documents__chamber'
    ).annotate(
        nb_proposals=Count('proposals'),
        nb_recomm=Count('proposals__recommendation')
    )
    sort_fields = {
        'title': 'title',
        'reference': 'reference',
        'nb_recomm': 'recommendations',
        'nb_proposals': 'proposals',
    }
    sort_default_field = 'nb_recomm'
    sort_default_dir = 'desc'

    def dossier_filter(self, qs):
        f = DossierFilter(self.request.GET, queryset=qs)
        self.current_filter = f
        return f.qs

    def get_queryset(self):
        qs = super(DossierList, self).get_queryset()
        qs = self.dossier_filter(qs)
        return qs

    def get_context_data(self, **kwargs):
        c = super(DossierList, self).get_context_data(**kwargs)
        c['filter'] = self.current_filter
        return c
