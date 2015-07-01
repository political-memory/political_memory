from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomeView(TemplateView):

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        return {
            'organization_name': 'La Quadrature du Net'
        }
