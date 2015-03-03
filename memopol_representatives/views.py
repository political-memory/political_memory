# from django.shortcuts import render
from django.views import generic


from memopol_representatives.models import MemopolRepresentative


class IndexView(generic.ListView):
    template_name = 'memopol_representatives/list.html'

    def get_queryset(self):
        return MemopolRepresentative.objects.all()
