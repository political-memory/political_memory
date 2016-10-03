# coding: utf-8

from django.db import models

from representatives_positions.models import Position

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailPositions(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_positions.html'

    def get_queryset(self):
        qs = super(RepresentativeDetailPositions, self).get_queryset()

        positions_qs = Position.objects.filter(published=True)
        theme = self.get_selected_theme()
        if theme:
            positions_qs = positions_qs.filter(themes__slug=theme)

        qs = qs.prefetch_related(
            models.Prefetch(
                'positions',
                queryset=positions_qs.order_by('-datetime', 'pk')
            ),
            'positions__themes',
            'positions__position_score'
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailPositions,
                  self).get_context_data(**kwargs)

        c['tab'] = 'positions'
        c['positions'] = c['object'].positions.all()

        return c
