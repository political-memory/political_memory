# coding: utf-8

from django.utils.text import slugify

from django_filters import FilterSet, MethodFilter, ModelChoiceFilter

from representatives.models import Chamber, Group, Representative


def chamber_filter(qs, value):
    return qs.filter(mandates__group__chamber=value)


def group_filter(qs, value):
    return qs.filter(mandates__group=value)


class RepresentativeFilter(FilterSet):

    search = MethodFilter(action='search_filter')

    chamber = ModelChoiceFilter(queryset=Chamber.objects.all(),
                                action=chamber_filter)

    country = ModelChoiceFilter(queryset=Group.objects.filter(kind='country'),
                                action=group_filter)

    class Meta:
        model = Representative
        fields = ['search', 'chamber', 'country']

    def search_filter(self, qs, value):
        if len(value) == 0:
            return qs

        return qs.filter(slug__icontains=slugify(value))
