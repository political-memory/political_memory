from rest_framework import (
    filters,
    viewsets,
)

from rql_filter.backend import RQLFilterBackend

from representatives.api import DefaultWebPagination

from .models import (
    DossierScore,
    RepresentativeScore,
    VoteScore
)

from .serializers import (
    DossierScoreSerializer,
    RepresentativeScoreSerializer,
    VoteScoreSerializer
)


class DossierScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view representative score contribution for each dossier
    """
    queryset = DossierScore.objects.all()
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'dossier': ['exact'],
        'representative': ['exact'],
        'score': ['exact', 'gte', 'lte']
    }
    search_fields = ('dossier', 'representative')
    ordering_fields = ('representative', 'dossier')
    pagination_class = DefaultWebPagination
    serializer_class = DossierScoreSerializer


class RepresentativeScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view representative scores
    """
    queryset = RepresentativeScore.objects.select_related('representative')
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'representative': ['exact'],
        'score': ['exact', 'gte', 'lte']
    }
    search_fields = ('representative', 'score')
    ordering_fields = ('representative', 'score')
    pagination_class = DefaultWebPagination
    serializer_class = RepresentativeScoreSerializer


class VoteScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view votes with their score impact.
    This endpoint only shows votes that have a matching recommendation.
    """
    queryset = VoteScore.objects.select_related(
        'vote__representative',
        'vote__proposal',
        'vote__proposal__dossier',
        'vote__proposal__recommendation'
    ).filter(
        vote__proposal__recommendation__isnull=False
    )

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )

    filter_fields = {
        'vote__representative': ['exact'],
        'vote__proposal': ['exact'],
        'vote__proposal__dossier': ['exact']
    }

    pagination_class = DefaultWebPagination
    serializer_class = VoteScoreSerializer
