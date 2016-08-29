# coding: utf-8

from django.views import generic

from representatives_votes.models import Dossier

from representatives_positions.views import PositionFormMixin


class DossierDetailBase(PositionFormMixin, generic.DetailView):
    template_name = 'representatives_votes/dossier_detail.html'

    queryset = Dossier.objects.prefetch_related('themes')
