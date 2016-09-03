# coding: utf-8

from django.views import generic

from representatives_positions.views import PositionFormMixin


class HomeView(PositionFormMixin, generic.TemplateView):
    template_name = 'home.html'
