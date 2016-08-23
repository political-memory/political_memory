# coding: utf-8

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailMandates(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_mandates.html'

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailMandates,
                  self).get_context_data(**kwargs)

        c['tab'] = 'mandates'
        c['mandates'] = c['object'].mandates.all()

        return c
