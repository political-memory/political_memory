from representatives.models import Representative

PERSONAL_FIELDS = ("first_name", "last_name", "full_name", "birth_place", "cv")
GENDER_DICT = dict(Representative.GENDER)


def export_a_representative(representative):
    reps = {"id": representative.remote_id}
    reps["personal"] = {field: getattr(representative, field) for field in PERSONAL_FIELDS}
    reps["personal"]["gender"] = GENDER_DICT[representative.gender]
    reps["personal"]["birth_date"] = representative.birth_date.strftime("%F") if representative.birth_date else None

    reps["contact"] = {}
    reps["contact"]["emails"] = [{"email": email.email, "type": email.kind} for email in representative.email_set.all()]
    reps["contact"]["websites"] = [{"website": website.url, "type": website.kind} for website in representative.website_set.all()]
    reps["contact"]["phones"] = [{"phone": phone.number, "type": phone.kind, "address": phone.address_id, "id": phone.id} for phone in representative.phone_set.all()]

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
        "name": mandate.name,
        "type": mandate.kind,
        "short_id": mandate.short_id,
        "url_official": mandate.url,
        "constituency": mandate.constituency,
        "role": mandate.role,
        "begin_date": mandate.begin_date.strftime("%F") if mandate.begin_date else None,
        "end_date": mandate.end_date.strftime("%F") if mandate.end_date else None,
        "current": mandate.active,
    } for mandate in representative.mandate_set.all()]

    return reps


def export_all_representatives():
    return [export_a_representative(representative) for representative in Representative.objects.all()]
