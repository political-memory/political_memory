from django.db import models

from rest_framework import (
    filters,
    pagination,
    renderers,
    viewsets,
)

from rql_filter.backend import RQLFilterBackend

from representatives.serializers import (
    ChamberSerializer,
    ConstituencySerializer,
    CountrySerializer,
    GroupSerializer,
    MandateSerializer,
    RepresentativeDetailSerializer,
    RepresentativeSerializer,
)

from .models import (
    Address,
    Chamber,
    Constituency,
    Country,
    Email,
    Group,
    Mandate,
    Phone,
    Representative,
    WebSite,
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
    queryset = Representative.objects.order_by('slug')
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'active': ['exact'],
        'slug': ['exact', 'icontains'],
        'id': ['exact'],
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'full_name': ['exact', 'icontains'],
        'gender': ['exact'],
        'birth_place': ['exact'],
        'birth_date': ['exact', 'gte', 'lte'],
    }
    search_fields = ('first_name', 'last_name', 'slug')
    pagination_class = DefaultWebPagination

    def get_queryset(self):
        qs = super(RepresentativeViewSet, self).get_queryset()
        qs = qs.prefetch_related(
            models.Prefetch(
                'email_set',
                queryset=Email.objects.order_by('id')
            ),
            models.Prefetch(
                'website_set',
                queryset=WebSite.objects.order_by('id')
            ),
            models.Prefetch(
                'address_set',
                queryset=Address.objects.select_related('country')
                                        .order_by('id')
            ),
            models.Prefetch(
                'phone_set',
                queryset=Phone.objects.select_related('address__country')
                                      .order_by('id')
            ),
            models.Prefetch(
                'mandates',
                queryset=Mandate.objects.order_by('id')
            )
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
    queryset = Mandate.objects.select_related('representative') \
                              .order_by('representative_id', 'id')
    serializer_class = MandateSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'id': ['exact'],
        'group__name': ['exact', 'icontains'],
        'group__abbreviation': ['exact'],
    }
    search_fields = ('group__name', 'group__abbreviation')


class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Constituency.objects.order_by('id')
    serializer_class = ConstituencySerializer

    filter_backends = (
        RQLFilterBackend,
    )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer

    filter_backends = (
        RQLFilterBackend,
    )


class ChamberViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Chamber.objects.order_by('id')
    serializer_class = ChamberSerializer

    filter_backends = (
        RQLFilterBackend,
    )


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = DefaultWebPagination
    queryset = Country.objects.order_by('id')
    serializer_class = CountrySerializer

    filter_backends = (
        RQLFilterBackend,
    )
