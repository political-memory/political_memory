# coding: utf-8

from django.views import generic

from representatives.models import Representative

from .representative_mixin import RepresentativeViewMixin


class RepresentativeMandates(RepresentativeViewMixin, generic.DetailView):
    template_name = 'representatives/representative_mandates'

    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeMandates, self).get_queryset()

        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeMandates, self).get_context_data(**kwargs)

        self.add_representative_country_and_main_mandate(c['object'])

        c['mandates'] = c['object'].mandates.all()

        return c
