from django.db import models

from rest_framework import (
    filters,
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
    queryset = Mandate.objects.all()
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

    def get_queryset(self):
        qs = super(MandateViewSet, self).get_queryset()
        qs = qs.select_related('representative')
        return qs


class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
