# coding: utf-8

from dal.autocomplete import Select2QuerySetView

from django.db.models import Q

from representatives.models import Group


class GroupAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Group.objects.exclude(kind__in=['chamber', 'country'])

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(abbreviation__icontains=self.q)
            )

        return qs
