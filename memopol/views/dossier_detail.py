# coding: utf-8

from django.views import generic

from representatives_votes.models import Dossier


class DossierDetail(generic.DetailView):

    queryset = Dossier.objects.prefetch_related(
        'proposals',
        'proposals__recommendation'
    )
