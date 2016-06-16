# coding: utf-8

from core.views import GridListMixin, PaginationMixin, CSVDownloadMixin, \
    ActiveLegislatureMixin

import datetime

from django.db import models
from django.utils.text import slugify
from django.views import generic

from representatives.models import Group, Representative

from ..filters import RepresentativeFilter
from .representative_mixin import RepresentativeViewMixin


class RepresentativeList(CSVDownloadMixin, GridListMixin, PaginationMixin,
                         RepresentativeViewMixin, ActiveLegislatureMixin,
                         generic.ListView):

    csv_name = 'representatives'
    queryset = Representative.objects.select_related('score')
    current_filter = None

    def get_context_data(self, **kwargs):
        c = super(RepresentativeList, self).get_context_data(**kwargs)

        c['filter'] = self.current_filter
        c['object_list'] = [
            self.add_representative_country_and_main_mandate(r)
            for r in c['object_list']
        ]

        return c

    def rep_filter(self, qs):
        f = RepresentativeFilter(self.request.GET, queryset=qs)
        self.current_filter = f
        return f.qs

    def get_queryset(self):
        qs = super(RepresentativeList, self).get_queryset()
        if self.get_active_only():
            qs = qs.filter(active=True)
        qs = self.rep_filter(qs)
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)
        return qs

    def get_csv_results(self, context, **kwargs):
        qs = self.get_queryset()
        qs = qs.prefetch_related('email_set')
        return [self.add_representative_country_and_main_mandate(r)
                for r in qs]

    def get_csv_row(self, obj):
        return (
            obj.full_name,
            u', '.join([e.email for e in obj.email_set.all()]),
            obj.main_mandate.group.abbreviation if obj.main_mandate else None,
            obj.country,
        )
