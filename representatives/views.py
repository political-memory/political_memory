import datetime

from django.db import models
from django.views import generic
from django.utils.text import slugify

from .models import Mandate, Group


class RepresentativeViewMixin(object):
    """
    A view mixin to add pre-fetched main_mandate and country to Representative

    If a Representative was fetched from a QuerySet that have been through
    prefetch_for_representative_country_and_main_mandate(), then
    add_representative_country_and_main_mandate(representative) adds the
    ``.country`` and ``.main_mandate`` properties "for free" - the prefetch
    methods adds an extra query, but gets all.
    """

    def prefetch_for_representative_country_and_main_mandate(self, queryset):
        """
        Prefetch Mandates with their Group and Constituency with Country.
        """
        mandates = Mandate.objects.order_by(
            '-end_date').select_related('constituency__country', 'group',
            'group__chamber')
        return queryset.prefetch_related(
            models.Prefetch('mandates', queryset=mandates))

    def add_representative_country_and_main_mandate(self, representative):
        """
        Set representative country, main_mandate and chamber.

        Note that this will butcher your database if you don't use
        self.prefetch_related.
        """
        today = datetime.date.today()

        representative.country = None
        representative.main_mandate = None

        for m in representative.mandates.all():
            if m.constituency.country_id and not representative.country:
                representative.country = m.constituency.country

            if ((m.end_date is None or m.end_date > today) and
                    m.group.kind == 'group' and
                    not representative.main_mandate):

                representative.main_mandate = m

            if representative.country and representative.main_mandate:
                break

        if representative.main_mandate:
            representative.chamber = representative.main_mandate.group.chamber

        return representative


class RepresentativeList(RepresentativeViewMixin, generic.ListView):
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
        qs = self.group_filter(qs)
        qs = self.search_filter(qs)
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)
        return qs


class RepresentativeDetail(RepresentativeViewMixin, generic.DetailView):
    def get_queryset(self):
        qs = super(RepresentativeDetail, self).get_queryset()
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)
        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)

        self.add_representative_country_and_main_mandate(c['object'])

        c['votes'] = c['object'].votes.all()
        c['mandates'] = c['object'].mandates.all()
        c['positions'] = c['object'].positions.filter(
            published=True).prefetch_related('tags')

        return c


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
