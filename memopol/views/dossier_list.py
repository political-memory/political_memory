# coding: utf-8

from core.views import PaginationMixin

from django.db.models import Count
from django.views import generic

from representatives_votes.models import Dossier

from ..filters import DossierFilter


class DossierList(PaginationMixin, generic.ListView):

    current_filter = None
    queryset = Dossier.objects.prefetch_related(
        'proposals',
        'proposals__recommendation',
        'documents',
        'documents__chamber'
    ).annotate(
        nb_proposals=Count('proposals'),
        nb_recomm=Count('proposals__recommendation')
    ).order_by('-nb_recomm', '-reference')

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
