# coding: utf-8

from django.db import models
from django.views import generic

from representatives.models import (Address, Chamber, Representative, Phone,
                                    WebSite)

from .representative_mixin import RepresentativeViewMixin

from representatives_positions.views import PositionFormMixin

from core.views import ThemeSelectionMixin


class RepresentativeDetailBase(RepresentativeViewMixin, PositionFormMixin,
                               ThemeSelectionMixin, generic.DetailView):

    queryset = Representative.objects.select_related('representative_score')

    def get_queryset(self):
        qs = super(RepresentativeDetailBase, self).get_queryset()

        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

        social = ['twitter', 'facebook']
        chambers = [c['abbreviation']
                    for c in Chamber.objects.values('abbreviation')]

        qs = qs.prefetch_related(
            'email_set',
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.filter(kind__in=social)
                                        .order_by('id'),
                to_attr='social_websites'
            ),
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.filter(kind__in=chambers)
                                        .order_by('id'),
                to_attr='chamber_websites'
            ),
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.exclude(kind__in=social)
                                        .exclude(kind__in=chambers)
                                        .order_by('id'),
                to_attr='other_websites'
            ),
            models.Prefetch(
                'address_set',
                queryset=Address.objects.select_related('country')
                                        .prefetch_related('phones')
                                        .order_by('id')
            ),
            models.Prefetch(
                'phone_set',
                queryset=Phone.objects.filter(address__isnull=True)
            ),
            'theme_scores__theme'
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailBase, self).get_context_data(**kwargs)

        self.add_representative_country_and_main_mandate(c['object'])
        c['position_form'].fields['representative'].initial = c['object'].pk

        return c
