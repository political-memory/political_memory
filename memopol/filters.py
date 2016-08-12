# coding: utf-8

import datetime

from django.db.models import Q
from django.utils.text import slugify

from django_filters import FilterSet, MethodFilter

from representatives.models import Representative
from representatives_votes.models import Dossier
from memopol_themes.models import Theme


class RepresentativeFilter(FilterSet):

    search = MethodFilter(action='search_filter')
    chamber = MethodFilter(action='chamber_filter')
    country = MethodFilter(action='group_filter')
    party = MethodFilter(action='group_filter')
    delegation = MethodFilter(action='group_filter')
    committee = MethodFilter(action='group_filter')

    class Meta:
        model = Representative
        fields = ['search', 'chamber', 'country', 'party', 'delegation',
                  'committee']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(slug__icontains=slugify(value))

    def chamber_filter(self, qs, value):
        if len(value) == 0:
            return qs

        today = datetime.date.today()
        return qs.filter(
            Q(mandates__end_date__gte=today) |
            Q(mandates__end_date__isnull=True),
            mandates__group__chamber=value
        )

    def group_filter(self, qs, value):
        if len(value) == 0:
            return qs

        today = datetime.date.today()
        return qs.filter(
            Q(mandates__end_date__gte=today) |
            Q(mandates__end_date__isnull=True),
            mandates__group=value
        )


class DossierFilter(FilterSet):

    search = MethodFilter(action='search_filter')
    chamber = MethodFilter(action='chamber_filter')

    class Meta:
        model = Dossier
        fields = ['search', 'chamber']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(Q(title__icontains=value) |
                         Q(reference__icontains=value))

    def chamber_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(documents__chamber=value)


class ThemeFilter(FilterSet):

    search = MethodFilter(action='search_filter')

    class Meta:
        model = Theme
        fields = ['search']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(Q(name__icontains=value) |
                         Q(description__icontains=value))
