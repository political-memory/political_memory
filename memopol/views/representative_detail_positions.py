# coding: utf-8

from django.db import models

from representatives_positions.models import Position

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailPositions(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_positions.html'

    def get_queryset(self):
        qs = super(RepresentativeDetailPositions, self).get_queryset()

        qs = qs.prefetch_related(
            models.Prefetch(
                'positions',
                queryset=Position.objects.filter(published=True)
                .order_by('-datetime', 'pk')
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
