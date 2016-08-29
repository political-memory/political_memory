# coding: utf-8

from core.views import PaginationMixin, SortMixin

from django.db.models import Count
from django.views import generic

from representatives_votes.models import Dossier

from ..filters import DossierFilter

from representatives_positions.views import PositionFormMixin


class DossierList(PaginationMixin, SortMixin, PositionFormMixin,
                  generic.ListView):

    current_filter = None
    queryset = Dossier.objects.prefetch_related(
        'documents__chamber',
        'themes'
    ).annotate(
        nb_proposals=Count('proposals', distinct=True),
        nb_recommendations=Count('proposals__recommendation', distinct=True),
        nb_documents=Count('documents', distinct=True)
    )
    sort_fields = {
        'title': 'title',
        'nb_recommendations': 'recommendations',
        'nb_proposals': 'proposals',
    }
    sort_default_field = 'nb_recommendations'
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
        c['view'] = 'dossier_list'
        c['filter'] = self.current_filter
        return c
