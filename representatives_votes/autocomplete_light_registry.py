import autocomplete_light.shortcuts as al

from .models import Proposal


al.register(Proposal, search_fields=['title'])
