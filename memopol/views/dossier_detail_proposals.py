# coding: utf-8

from .dossier_detail_base import DossierDetailBase


class DossierDetailProposals(DossierDetailBase):
    template_name = 'representatives_votes/dossier_detail_proposals.html'

    def get_queryset(self):
        qs = super(DossierDetailProposals, self).get_queryset()
        qs = qs.prefetch_related(
            'proposals__recommendation',
            'proposals__dossier__documents__chamber'
        )
        return qs

    def get_context_data(self, **kwargs):
        c = super(DossierDetailProposals, self).get_context_data(**kwargs)

        c['tab'] = 'proposals'
        c['proposals'] = c['object'].proposals.all()

        return c
