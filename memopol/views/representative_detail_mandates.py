# coding: utf-8

from django.db.models import IntegerField, Case, Value, When

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailMandates(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_mandates.html'

    mandates_order = ['chamber', 'country', 'committee', 'delegation']

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailMandates,
                  self).get_context_data(**kwargs)

        c['tab'] = 'mandates'
        c['mandates'] = c['object'].mandates.annotate(
            weight=Case(
                When(group__kind='chamber', then=Value(1)),
                When(group__kind='country', then=Value(2)),
                When(group__kind='group', then=Value(3)),
                When(group__kind='committee', then=Value(4)),
                default=Value(100),
                output_field=IntegerField()
            )
        ).select_related('group__chamber').order_by('-end_date', 'weight')

        return c
