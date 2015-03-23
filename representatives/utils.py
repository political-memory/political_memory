import sys

from django.db import transaction
from datetime import datetime

from representatives.models import Representative, Country, Group, Constituency

PERSONAL_FIELDS = ("first_name", "last_name", "full_name", "birth_place", "cv", "photo")
GENDER_DICT = dict(Representative.GENDER)


def export_a_representative(representative):
    reps = {"id": representative.remote_id}
    reps["personal"] = {field: getattr(representative, field) for field in PERSONAL_FIELDS}
    reps["personal"]["gender"] = GENDER_DICT[representative.gender]
    reps["personal"]["birth_date"] = representative.birth_date.strftime("%F") if representative.birth_date else None

    reps["contact"] = {}

    reps["contact"]["emails"] = [{
        "email": email.email,
        "type": email.kind
    } for email in representative.email_set.all()]

    reps["contact"]["websites"] = [{
        "website": website.url,
        "type": website.kind
    } for website in representative.website_set.all()]

    reps["contact"]["phones"] = [{
        "phone": phone.number,
        "type": phone.kind, "address":
        phone.address_id,
        "id": phone.id
    } for phone in representative.phone_set.all()]

    reps["contact"]["address"] = [{
       "id": address.id,
       "country": {"name": address.country.name, "code": address.country.code},
       "city": address.city,
       "street": address.street,
       "number": address.number,
       "postcode": address.postcode,
       "floor": address.floor,
       "office_number": address.office_number,
       "type": address.kind,
       "geo": None,
       "phones": [phone.id for phone in address.phone_set.all()],
    } for address in representative.address_set.all()]

    reps["mandates"] = [{
        "name": mandate.group.name,
        "type": mandate.group.kind,
        "short_id": mandate.group.abbreviation,
        "url_official": mandate.url,
        "constituency": mandate.constituency.name,
        "role": mandate.role,
        "begin_date": mandate.begin_date.strftime("%F") if mandate.begin_date else None,
        "end_date": mandate.end_date.strftime("%F") if mandate.end_date else None,
        "current": mandate.active,
    } for mandate in representative.mandate_set.all()]

    return reps


def export_all_representatives():
    return [export_a_representative(representative) for representative in Representative.objects.all()]


def import_representatives_from_format(data, verbose=False):
    reverted_gender_dict = {x[1]: x[0] for x in Representative.GENDER}
    a = 0
    end = len(data)

    with transaction.atomic():
        for reps in data:
            a += 1
            if verbose:
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
            representative.cv = reps["personal"]["cv"]
            representative.photo = reps["personal"]["photo"]

            if reps["personal"]["birth_date"]:
                representative.birth_date = datetime.strptime(reps["personal"]["birth_date"], "%Y-%m-%d")
            else:
                representative.birth_date = None

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

                constituency, created = Constituency.objects.get_or_create(
                    name=mandate['constituency']
                )

                group, created = Group.objects.get_or_create(
                    name=mandate['name'],
                    abbreviation=mandate['short_id'],
                    kind=mandate['type']
                )

                representative.mandate_set.create(
                    group=group,
                    constituency=constituency,
                    url=mandate["url_official"],
                    role=mandate["role"],
                    begin_date=mandate["begin_date"],
                    end_date=mandate["end_date"],
                    # active=mandate["current"],
                )

            representative.save()

    if verbose:
        sys.stdout.write("\n")
