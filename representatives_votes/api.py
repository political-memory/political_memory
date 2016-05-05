from .models import (
    Dossier,
    Proposal,
    Vote
)

from rest_framework import (
    filters,
    viewsets,
)

from representatives.api import DefaultWebPagination

from representatives_votes.serializers import (
    DossierDetailSerializer,
    DossierSerializer,
    ProposalDetailSerializer,
    ProposalSerializer,
    VoteSerializer,
)


class DossierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows dossiers to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'fingerprint': ['exact'],
        'title': ['exact', 'icontains'],
        'reference': ['exact', 'icontains'],
    }

    search_fields = (
        'title',
        'fingerprint',
        'reference',
        'text',
        'proposals__title'
    )

    ordering_fields = ['reference']

    def retrieve(self, request, pk=None):
        self.serializer_class = DossierDetailSerializer
        self.queryset = self.queryset.prefetch_related('proposals')
        return super(DossierViewSet, self).retrieve(request, pk)


class ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows proposals to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'fingerprint': ['exact'],
        'dossier__fingerprint': ['exact'],
        'title': ['exact', 'icontains'],
        'description': ['icontains'],
        'reference': ['exact', 'icontains'],
        'datetime': ['exact', 'gte', 'lte'],
        'kind': ['exact'],
    }

    search_fields = (
        'title',
        'fingerprint', 'reference',
        'dossier__fingerprint',
        'dossier__title',
        'dossier__reference'
    )

    ordering_fields = ['reference']

    def retrieve(self, request, pk=None):
        self.serializer_class = ProposalDetailSerializer
        return super(ProposalViewSet, self).retrieve(request, pk)


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows proposals to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Vote.objects.select_related('representative', 'proposal')
    serializer_class = VoteSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'proposal__fingerprint': ['exact'],
        'position': ['exact'],
        'representative_name': ['exact', 'icontains'],
        'representative': ['exact']
    }
