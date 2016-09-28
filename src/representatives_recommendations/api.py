from rest_framework import (
    filters,
    viewsets,
)

from rql_filter.backend import RQLFilterBackend

from representatives.api import DefaultWebPagination

from .models import Recommendation

from .serializers import RecommendationSerializer


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows recommendations to be viewed.
    """
    queryset = Recommendation.objects.select_related('proposal')
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'id': ['exact'],
        'recommendation': ['exact'],
        'title': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'weight': ['exact', 'gte', 'lte']
    }
    search_fields = ('title', 'description')
    ordering_fields = ('id', 'weight', 'title')
    pagination_class = DefaultWebPagination
    serializer_class = RecommendationSerializer
