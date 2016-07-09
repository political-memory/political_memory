# coding: utf-8

from dal.autocomplete import ModelSelect2

import datetime

from django.db.models import Q
from django.utils.text import slugify

from django_filters import FilterSet, MethodFilter, ModelChoiceFilter

from representatives.models import Chamber, Group, Representative
from representatives_votes.models import Dossier


def rep_chamber_filter(qs, value):
    today = datetime.date.today()
    return qs.filter(
        Q(mandates__end_date__gte=today) | Q(mandates__end_date__isnull=True),
        mandates__group__chamber=value
    )


def dossier_chamber_filter(qs, value):
    return qs.filter(documents__chamber=value)


def group_filter(qs, value):
    today = datetime.date.today()
    return qs.filter(
        Q(mandates__end_date__gte=today) | Q(mandates__end_date__isnull=True),
        mandates__group=value
    )


class RepresentativeFilter(FilterSet):

    search = MethodFilter(action='search_filter')

    chamber = ModelChoiceFilter(queryset=Chamber.objects.all(),
                                action=rep_chamber_filter)

    country = ModelChoiceFilter(queryset=Group.objects.filter(kind='country'),
                                action=group_filter)

    group = ModelChoiceFilter(queryset=Group.objects.exclude(
                              kind__in=['chamber', 'country']),
                              action=group_filter,
                              widget=ModelSelect2(url='group-autocomplete'),
                              label='Party, committee or delegation')

    class Meta:
        model = Representative
        fields = ['search', 'chamber', 'country']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(slug__icontains=slugify(value))


class DossierFilter(FilterSet):

    search = MethodFilter(action='search_filter')

    chamber = ModelChoiceFilter(queryset=Chamber.objects.all(),
                                action=dossier_chamber_filter)

    class Meta:
        model = Dossier
        fields = ['search', 'chamber']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(Q(title__icontains=value) |
                         Q(reference__icontains=value))
