# coding: utf-8

from core.views import PaginationMixin

from django.db.models import Count
from django.views import generic

from representatives_votes.models import Dossier


class DossierList(PaginationMixin, generic.ListView):

    queryset = Dossier.objects.prefetch_related(
        'proposals',
        'proposals__recommendation'
    ).annotate(
        nb_recomm=Count('proposals__recommendation')
    ).order_by('-nb_recomm', '-reference')
