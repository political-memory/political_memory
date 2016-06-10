# coding: utf-8

from core.views import GridListMixin, PaginationMixin, CSVDownloadMixin, \
    ActiveLegislatureMixin

import datetime

from django.db import models
from django.utils.text import slugify
from django.views import generic

from representatives.models import Group, Representative

from .representative_mixin import RepresentativeViewMixin


class RepresentativeList(CSVDownloadMixin, GridListMixin, PaginationMixin,
                         RepresentativeViewMixin, ActiveLegislatureMixin,
                         generic.ListView):

    csv_name = 'meps.csv'
    queryset = Representative.objects.select_related('score')

    def get_context_data(self, **kwargs):
        c = super(RepresentativeList, self).get_context_data(**kwargs)

        c['object_list'] = [
            self.add_representative_country_and_main_mandate(r)
            for r in c['object_list']
        ]

        return c

    def search_filter(self, qs):
        search = self.request.GET.get('search', None)
        if search:
            qs = qs.filter(slug__icontains=slugify(search))
        return qs

    def group_filter(self, qs):
        group_kind = self.kwargs.get('group_kind', None)
        chamber = self.kwargs.get('chamber', None)
        group = self.kwargs.get('group', None)
        today = datetime.date.today()

        if group_kind and group:
            if group.isnumeric():
                group_qs = Group.objects.filter(
                    id=int(group)
                )
            else:
                group_qs = Group.objects.filter(
                    name=group,
                    kind=group_kind
                )

            if chamber:
                group_qs = group_qs.filter(chamber__name=chamber)

            qs = qs.filter(
                models.Q(mandates__end_date__gte=today) |
                models.Q(mandates__end_date__isnull=True),
                mandates__group__in=group_qs
            )

        return qs

    def get_queryset(self):
        qs = super(RepresentativeList, self).get_queryset()
        if self.get_active_only():
            qs = qs.filter(active=True)
        qs = self.group_filter(qs)
        qs = self.search_filter(qs)
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)
        return qs

    def get_csv_results(self, context, **kwargs):
        qs = super(RepresentativeList, self).get_queryset()
        qs = qs.prefetch_related('email_set')
        return [self.add_representative_country_and_main_mandate(r)
                for r in qs]

    def get_csv_row(self, obj):
        return (
            obj.full_name,
            u', '.join([e.email for e in obj.email_set.all()]),
            obj.main_mandate.group.abbreviation,
            obj.country,
        )
