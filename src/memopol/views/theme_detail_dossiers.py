# coding: utf-8

from django.db import models

from representatives_votes.models import Dossier

from .theme_detail_base import ThemeDetailBase


class ThemeDetailDossiers(ThemeDetailBase):
    template_name = 'memopol_themes/theme_detail_dossiers.html'

    def get_queryset(self):
        qs = super(ThemeDetailDossiers, self).get_queryset()
        qs = qs.prefetch_related(
            models.Prefetch(
                'dossiers',
                Dossier.objects.order_by('-pk')
                .prefetch_related('documents__chamber', 'themes')
                .annotate(
                    nb_proposals=models.Count('proposals', distinct=True),
                    nb_recommendations=models.Count(
                        'proposals__recommendation', distinct=True),
                    nb_documents=models.Count('documents', distinct=True)
                )
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        c = super(ThemeDetailDossiers, self).get_context_data(**kwargs)

        c['tab'] = 'dossiers'
        c['dossiers'] = c['object'].dossiers.all()

        return c
