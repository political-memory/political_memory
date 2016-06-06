# coding: utf-8

from django.db import models
from django.views import generic

from representatives.models import Representative, Address, Phone, WebSite
from representatives_positions.forms import PositionForm
from representatives_recommendations.models import VoteScore
from representatives_votes.models import Proposal

from .representative_mixin import RepresentativeViewMixin


class RepresentativeDetail(RepresentativeViewMixin, generic.DetailView):

    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeDetail, self).get_queryset()

        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

        social = ['twitter', 'facebook']
        qs = qs.prefetch_related(
            'email_set',
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.filter(kind__in=social),
                to_attr='social_websites'
            ),
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.exclude(kind__in=social),
                to_attr='other_websites'
            ),
            models.Prefetch(
                'address_set',
                queryset=Address.objects.select_related('country')
            ),
            models.Prefetch(
                'phone_set',
                queryset=Phone.objects.select_related('address__country')
            ),
            models.Prefetch(
                'votes',
                queryset=VoteScore.objects.filter(
                    proposal__in=Proposal.objects.exclude(recommendation=None),
                ).select_related('proposal__recommendation').order_by(
                    '-proposal__datetime')
            )
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)

        self.add_representative_country_and_main_mandate(c['object'])

        c['votes'] = c['object'].votes.all()
        c['mandates'] = c['object'].mandates.all()
        c['positions'] = c['object'].positions.filter(
            published=True).prefetch_related('tags')

        c['position_form'] = PositionForm(
            initial={'representative': self.object.pk})
        self.add_representative_country_and_main_mandate(c['object'])

        return c
