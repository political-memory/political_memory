from django.views import generic
from django.db import models

from representatives.views import RepresentativeViewMixin
from representatives.models import Mandate

from .models import Position
from .forms import PositionForm


class PositionCreate(generic.CreateView):
    model = Position
    form_class = PositionForm

    def get_success_url(self):
        return self.object.representative.get_absolute_url()


class PositionDetail(RepresentativeViewMixin, generic.DetailView):
    queryset = Position.objects.filter(published=True).select_related(
        'representative__score')

    def get_queryset(self):
        qs = super(PositionDetail, self).get_queryset()
        qs = qs.prefetch_related(models.Prefetch(
            'representative__mandates',
            Mandate.objects.select_related('constituency__country', 'group')
        ))
        return qs

    def get_object(self):
        obj = super(PositionDetail, self).get_object()
        self.add_representative_country_and_main_mandate(obj.representative)
        return obj
