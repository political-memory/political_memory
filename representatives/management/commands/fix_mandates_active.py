import datetime
from django.core.management.base import BaseCommand
from representatives.models import Mandate


class Command(BaseCommand):

    def handle(self, *args, **options):
        date = datetime.datetime.now().date()
        for mandate in Mandate.objects.all():
            mandate.active = mandate.end_date > date
            mandate.save()
