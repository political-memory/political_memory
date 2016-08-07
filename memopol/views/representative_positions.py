# coding: utf-8

from django.db import models
from django.views import generic

from representatives.models import Representative
from representatives_positions.forms import PositionForm
from representatives_positions.models import Position

from .representative_mixin import RepresentativeViewMixin


class RepresentativePositions(RepresentativeViewMixin, generic.DetailView):
    template_name = 'representatives/representative_positions'

    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativePositions, self).get_queryset()

        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

        qs = qs.prefetch_related(
            models.Prefetch(
                'positions',
                queryset=Position.objects.filter(published=True)
                .order_by('-datetime', 'pk')
            )
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativePositions, self).get_context_data(**kwargs)

        c['position_form'] = PositionForm(
            initial={'representative': self.object.pk})
        self.add_representative_country_and_main_mandate(c['object'])

        return c
