import datetime

from django.db import models

from .models import Mandate


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
            '-end_date').select_related('constituency__country', 'group')
        return queryset.prefetch_related(
            models.Prefetch('mandates', queryset=mandates))

    def add_representative_country_and_main_mandate(self, representative):
        """
        Set representative country and main_mandate.

        Note that this will butcher your database if you don't use
        self.prefetch_related.
        """
        today = datetime.date.today()

        representative.country = None
        representative.main_mandate = None

        for m in representative.mandates.all():
            if m.constituency.country_id and not representative.country:
                representative.country = m.constituency.country

            if (m.end_date > today and m.group.kind == 'group' and
                not representative.main_mandate):

                representative.main_mandate = m

            if representative.country and not representative.main_mandate:
                break

        return representative
