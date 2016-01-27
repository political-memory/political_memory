from django.conf.urls import include, url

from rest_framework import routers

from representatives.api import (
    ConstituencyViewSet,
    GroupViewSet,
    MandateViewSet,
    RepresentativeViewSet,
)

router = routers.DefaultRouter()
router.register(r'constituencies', ConstituencyViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'mandates', MandateViewSet)
router.register(r'representatives', RepresentativeViewSet)

urlpatterns = [
    url(r'api/', include(router.urls)),
]
