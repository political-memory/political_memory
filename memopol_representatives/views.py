# from django.shortcuts import render
from django.views import generic

from representatives.models import Representative


class IndexView(generic.ListView):
    template_name = 'memopol_representatives/list.html'

    def get_queryset(self):
        return Representative.objects.all()
