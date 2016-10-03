# coding: utf-8

from .dossier_detail_base import DossierDetailBase


class DossierDetailDocuments(DossierDetailBase):
    template_name = 'representatives_votes/dossier_detail_documents.html'

    def get_queryset(self):
        qs = super(DossierDetailDocuments, self).get_queryset()
        qs = qs.prefetch_related('documents__chamber')
        return qs

    def get_context_data(self, **kwargs):
        c = super(DossierDetailDocuments, self).get_context_data(**kwargs)

        c['tab'] = 'documents'
        c['documents'] = c['object'].documents.all()

        return c
