# Project specific "glue" coupling of all apps
from django.db import models
from django.db.models import Count
from django.utils.http import urlencode

from core.views import GridListMixin, PaginationMixin, CSVDownloadMixin
from representatives import views as representatives_views
from representatives.models import Representative
from representatives_votes import views as representatives_votes_views
from representatives_votes.models import Dossier, Proposal
from representatives_positions.forms import PositionForm
from representatives_recommendations.models import ScoredVote


class PaginationFormMixin(PaginationMixin):
    """
    Only add an searchparameters to the context to make it easy to paginate
    without duplicating the 'page' parameter and keeping the form's GET parameters.
    """
    def get_context_data(self, **kwargs):
        c = super(PaginationFormMixin, self).get_context_data(**kwargs)
        params = [(k,v) for k, v in self.request.GET.iteritems() if k != 'page']
        c['searchparameters'] = urlencode(dict(params))
        return c


class RepresentativeList(CSVDownloadMixin,
                         GridListMixin,
                         PaginationFormMixin,
                         representatives_views.RepresentativeList):
    queryset = Representative.objects.filter(active=True).select_related('score')
    csv_name = 'meps.csv'

    def get_csv_results(self, context, **kwargs):
        qs = super(RepresentativeList, self).get_queryset()
        qs = qs.prefetch_related('email_set')
        return [self.add_representative_country_and_main_mandate(r)
                for r in qs]

    def get_csv_row(self, obj):
        return (
            obj.full_name,
            u', '.join([e.email for e in obj.email_set.all()]),
            obj.main_mandate.group.abbreviation,
            obj.country,
        )

    def get_context_data(self, **kwargs):
        c = super(RepresentativeList, self).get_context_data(**kwargs)
        group = self.kwargs.get('group', None)
        group_kind = self.kwargs.get('group_kind', None)
        c['search'] = {
            'search': self.request.GET.get('search', None),
            group_kind: group,
        }
        return c


class RepresentativeDetail(representatives_views.RepresentativeDetail):
    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeDetail, self).get_queryset()
        votes = (ScoredVote.objects.filter(
            proposal__in=Proposal.objects.exclude(recommendation=None))
                 .select_related('proposal__recommendation')
                 .select_related('proposal__dossier'))

        qs = qs.prefetch_related(models.Prefetch('votes', queryset=votes))
        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)
        c['position_form'] = PositionForm(
            initial={'representative': self.object.pk})
        self.add_representative_country_and_main_mandate(c['object'])
        return c


class DossierList(PaginationFormMixin, representatives_votes_views.DossierList):
    queryset = Dossier.objects.filter(proposals__recommendation__isnull=False)

    def get_queryset(self):
        qs = super(DossierList, self).get_queryset()
        return qs.annotate(votes_count=Count('proposals__votes'))


class DossierDetail(representatives_votes_views.DossierDetail):

    def get_context_data(self, **kwargs):
        c = super(DossierDetail, self).get_context_data(**kwargs)
        c['proposals'] = (c['dossier'].proposals.filter(recommendation__isnull=False)
                                                .select_related('recommendation'))

        # Note: this is a bit of a hack, we feed the RelatedManager with
        # the prefetch_related with a clause, so that representative.votes.all
        # doesn't query the db but returns what he has in store.
        votes = (ScoredVote.objects
                 .filter(proposal__in=c['proposals'])
                 .select_related('proposal__recommendation'))
        c['representatives'] = (Representative.objects
                                .filter(votes__proposal__in=c['proposals'])
                                .distinct()
                                .prefetch_related(models.Prefetch('votes', queryset=votes)))

        return c
