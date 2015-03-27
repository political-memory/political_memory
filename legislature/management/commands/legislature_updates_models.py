# import datetime
from django.core.management.base import BaseCommand
from representatives import models
from legislature.models import MRepresentative, MMandate, MGroup

from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        # Representatives
        print('Representatives')
        n = models.Representative.objects.all().count()
        for i, representative in enumerate(models.Representative.objects.all()):
            mrepresentative = MRepresentative(representative_ptr=representative)
            mrepresentative.__dict__.update(representative.__dict__)
            mrepresentative.save()
            print("%s/%s\r" % (i, n)),

        print('Mandates')
        for i, mrepresentative in enumerate(MRepresentative.objects.all()):
            representative = mrepresentative.representative_ptr
            for mandate in representative.mandate_set.all():
                mmandate = MMandate(mandate_ptr=mandate)
                mmandate.__dict__.update(mandate.__dict__)
                mmandate.mrepresentative = mrepresentative

                # Group creation
                try:
                    mgroup = MGroup.objects.get(group_ptr=mandate.group)
                except MGroup.DoesNotExist:
                    mgroup = MGroup(group_ptr=mandate.group)
                    mgroup.__dict__.update(mandate.group.__dict__)
                    mgroup.save()
                #print(mgroup)

                mmandate.mgroup = mgroup
                mmandate.save()
                mmandate.update_active()

            mrepresentative.update_country()
            mrepresentative.update_active()
            mrepresentative.save()
            print("%s/%s\r" % (i, n)),

        print('Groups')
        for i, mgroup in enumerate(MGroup.objects.all()):
            mgroup.update_active()
