from django.db import models

from rest_framework import (
    filters,
    pagination,
    renderers,
    viewsets,
)

from representatives.serializers import (
    ConstituencySerializer,
    GroupSerializer,
    MandateSerializer,
    RepresentativeDetailSerializer,
    RepresentativeSerializer,
)

from .models import (
    Address,
    Constituency,
    Group,
    Mandate,
    Phone,
    Representative,
)


class DefaultWebPagination(pagination.PageNumberPagination):
    default_web_page_size = 10

    def get_page_size(self, request):
        web = isinstance(request.accepted_renderer,
                         renderers.BrowsableAPIRenderer)
        size = pagination.PageNumberPagination.get_page_size(self, request)

        if web and not size:
            return self.default_web_page_size

        return size


class RepresentativeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows representatives to be viewed.
    """
    queryset = Representative.objects.all()
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = {
        'active': ['exact'],
        'slug': ['exact', 'icontains'],
        'id': ['exact'],
        'remote_id': ['exact'],
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'full_name': ['exact', 'icontains'],
        'gender': ['exact'],
        'birth_place': ['exact'],
        'birth_date': ['exact', 'gte', 'lte'],
    }
    search_fields = ('first_name', 'last_name', 'slug')
    ordering_fields = ('id', 'birth_date', 'last_name', 'full_name')
    pagination_class = DefaultWebPagination

    def get_queryset(self):
        qs = super(RepresentativeViewSet, self).get_queryset()
        qs = qs.prefetch_related(
            'email_set',
            'website_set',
            models.Prefetch(
                'address_set',
                queryset=Address.objects.select_related('country')
            ),
            models.Prefetch(
                'phone_set',
                queryset=Phone.objects.select_related('address__country')
            ),
            'mandates',
        )
        return qs

    def list(self, request):
        self.serializer_class = RepresentativeSerializer
        return super(RepresentativeViewSet, self).list(request)

    def retrieve(self, request, pk=None):
        self.serializer_class = RepresentativeDetailSerializer
        return super(RepresentativeViewSet, self).retrieve(request, pk)


class MandateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows mandates to be viewed.
    """
    pagination_class = DefaultWebPagination
    queryset = Mandate.objects.select_related('representative')
    serializer_class = MandateSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_fields = {
        'id': ['exact'],
        'group__name': ['exact', 'icontains'],
        'group__abbreviation': ['exact'],
    }
    search_fields = ('group__name', 'group__abbreviation')


class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
