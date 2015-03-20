# import datetime
from django.core.management.base import BaseCommand
from representatives import models
from legislature.models import Representative, Mandate

from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        # Representatives
        print('Representatives')
        n = models.Representative.objects.all().count()
        for i, representative in enumerate(models.Representative.objects.all()):
            legislature_representative = Representative(representative_ptr=representative)
            legislature_representative.__dict__.update(representative.__dict__)
            legislature_representative.update_country()
            legislature_representative.save()
            print("%s/%s\r" % (i, n)),

        print('Mandates')
        for i, representative in enumerate(Representative.objects.all()):
            legislature_mandates = []
            for mandate in representative.mandate_set.all():
                legislature_mandate = Mandate(mandate_ptr=mandate)
                legislature_mandate.__dict__.update(mandate.__dict__)
                legislature_mandate.update_active()
                legislature_mandate.save()
                legislature_mandates.append(legislature_mandate)
            representative.update_active()
            representative.save()
            print("%s/%s\r" % (i, n)),
