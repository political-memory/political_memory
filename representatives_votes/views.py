from django.views import generic

from .models import Dossier


class DossierList(generic.ListView):
    model = Dossier


class DossierDetail(generic.DetailView):
    model = Dossier
