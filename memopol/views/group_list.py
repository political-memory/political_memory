# coding: utf-8

import datetime

from core.views import PaginationMixin, ActiveLegislatureMixin

from django.db import models
from django.views import generic

from representatives.models import Group


class GroupList(PaginationMixin, ActiveLegislatureMixin, generic.ListView):

    def override_active_only(self):
        kind = self.kwargs.get('kind')

        if kind == 'chamber' or kind == 'country':
            return False
        else:
            return None

    def get_queryset(self):
        qs = Group.objects.all()

        if self.get_active_only():
            qs = qs.filter(
                models.Q(mandates__end_date__gte=datetime.date.today()) |
                models.Q(mandates__end_date__isnull=True)
            )

        kind = self.kwargs.get('kind', None)
        if kind:
            qs = qs.filter(kind=kind).distinct()

        return qs.select_related('chamber').order_by('chamber__name', 'name')
