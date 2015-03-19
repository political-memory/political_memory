import datetime
from django.core.management.base import BaseCommand
from representatives.models import Mandate
from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        date = datetime.datetime.now().date()
        mandates = Mandate.objects.all()
        n = len(mandates)
        for i, mandate in enumerate(mandates):
            mandate.active = mandate.end_date > date
            mandate.save()
            print("%s/%s\r" % (i, n)),
