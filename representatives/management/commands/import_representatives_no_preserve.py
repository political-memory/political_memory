import sys
import json

from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from representatives.models import Representative, Country

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        reverted_gender_dict = {x[1]: x[0] for x in Representative.GENDER}
        data = json.load(sys.stdin)
        a = 0
        end = len(data)
        with transaction.commit_on_success():
            for reps in data:
                a += 1
                sys.stdout.write("%s/%s\r" % (a, end))
                sys.stdout.flush()
                remote_id = reps["id"]
                representative = Representative.objects.filter(remote_id=remote_id)
                if representative:
                    representative = representative[0]
                else:
                    representative = Representative()
                    representative.remote_id = remote_id

                representative.first_name = reps["personal"]["first_name"]
                representative.last_name = reps["personal"]["last_name"]
                representative.full_name = reps["personal"]["full_name"]
                representative.birth_place = reps["personal"]["birth_place"]
                representative.birth_date = datetime.strptime(reps["personal"]["birth_date"], "%Y-%m-%d") if reps["personal"]["birth_date"] else None
                representative.cv = reps["personal"]["cv"]
                representative.gender = reverted_gender_dict[reps["personal"]["gender"]]

                representative.save()

                representative.email_set.all().delete()
                for email in reps["contact"]["emails"]:
                    representative.email_set.create(
                        email=email["email"],
                        kind=email["type"],
                    )

                representative.website_set.all().delete()
                for website in reps["contact"]["websites"]:
                    representative.website_set.create(
                        url=website["website"],
                        kind=website["type"],
                    )

                addresses = {}
                representative.address_set.all().delete()
                for address in reps["contact"]["address"]:
                    country = Country.objects.filter(code=address["country"]["code"])
                    if not country:
                        country = Country.objects.create(
                            name=address["country"]["name"],
                            code=address["country"]["code"]
                        )
                    else:
                        country = country[0]

                    address_in_db = representative.address_set.create(
                        city=address["city"],
                        street=address["street"],
                        number=address["number"],
                        postcode=address["postcode"],
                        floor=address["floor"],
                        office_number=address["office_number"],
                        kind=address["type"],
                        country=country
                    )

                    for phone in address["phones"]:
                        addresses[phone] = address_in_db

                representative.phone_set.all().delete()
                for phone in reps["contact"]["phones"]:
                    representative.phone_set.create(
                        number=phone["phone"],
                        kind=phone["type"],
                        address=addresses[phone["id"]]
                    )

                representative.mandate_set.all().delete()
                for mandate in reps["mandates"]:
                    representative.mandate_set.create(
                        name=mandate["name"],
                        kind=mandate["type"],
                        short_id=mandate["short_id"],
                        url=mandate["url_official"],
                        constituency=mandate["constituency"],
                        role=mandate["role"],
                        begin_date=mandate["begin_date"],
                        end_date=mandate["end_date"],
                        active=mandate["current"],
                    )

                representative.save()

        sys.stdout.write("\n")
