# coding: utf-8

from core.views import ActiveLegislatureMixin

from dal.autocomplete import Select2QuerySetView

import datetime

from django.db.models import Q

from representatives.models import Group


class GroupAutocomplete(Select2QuerySetView, ActiveLegislatureMixin):

    def get_queryset(self):
        qs = Group.objects.distinct().exclude(kind__in=['chamber', 'country'])

        if self.get_active_only():
            qs = qs.filter(
                Q(mandates__end_date__gte=datetime.date.today()) |
                Q(mandates__end_date__isnull=True)
            )

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(abbreviation__icontains=self.q)
            )

        return qs
