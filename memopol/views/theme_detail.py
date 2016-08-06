# coding: utf-8

from django.views import generic

from memopol_themes.models import Theme


class ThemeDetail(generic.DetailView):
    queryset = Theme.objects.prefetch_related(
        'links',
        'dossiers__documents__chamber',
        'proposals__recommendation',
        'proposals__dossier__documents__chamber',
        'positions__representative',
    )
