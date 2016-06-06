# coding: utf-8

import datetime

from django.db import models
from django.views import generic

from representatives.models import Group


class GroupList(generic.ListView):

    def get_queryset(self):
        qs = Group.objects.filter(
            models.Q(mandates__end_date__gte=datetime.date.today()) |
            models.Q(mandates__end_date__isnull=True)
        )

        kind = self.kwargs.get('kind', None)
        if kind:
            qs = qs.filter(kind=kind).distinct()

        return qs.select_related('chamber').order_by('chamber__name', 'name')
