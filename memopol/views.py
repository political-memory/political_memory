# Project specific "glue" coupling of all apps
from django.db import models

from core.views import GridListMixin, PaginationMixin, CSVDownloadMixin
from representatives import views as representatives_views
from representatives.models import Representative
from representatives_votes import views as representatives_votes_views
from representatives_votes.models import Dossier
from representatives_positions.forms import PositionForm
from representatives_recommendations.models import ScoredVote


class RepresentativeList(
    CSVDownloadMixin,
    GridListMixin,
    PaginationMixin,
    representatives_views.RepresentativeList
):

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

    queryset = Representative.objects.filter(
        active=True).select_related('score')


class RepresentativeDetail(representatives_views.RepresentativeDetail):
    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeDetail, self).get_queryset()
        votes = ScoredVote.objects.select_related('proposal__recommendation')
        qs = qs.prefetch_related(models.Prefetch('votes', queryset=votes))
        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetail, self).get_context_data(**kwargs)
        c['position_form'] = PositionForm(
            initial={'representative': self.object.pk})
        self.add_representative_country_and_main_mandate(c['object'])
        return c


class DossierList(PaginationMixin, representatives_votes_views.DossierList):
    queryset = Dossier.objects.exclude(proposals__recommendation=None)
