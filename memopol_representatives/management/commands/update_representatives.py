from django.core.management.base import BaseCommand
from django.db import transaction

from memopol.utils import progress_bar
from representatives.models import Representative
from memopol_representatives.models import MemopolRepresentative

class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        n = Representative.objects.all().count()
        for i, representative in enumerate(Representative.objects.all()):
            memopol_representative = MemopolRepresentative(representative_ptr=representative)
            memopol_representative.__dict__.update(representative.__dict__)
            # Auto set active flag of the memopol representative
            memopol_representative.update_active()
            progress_bar(i, n)
