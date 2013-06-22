import json
from representatives.models import Representative
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        result = []
        personal_fields = ("first_name", "last_name", "full_name", "birth_place", "cv")
        gender_dict = dict(Representative.GENDER)
        for representative in Representative.objects.all():
            reps = {"id": representative.remote_id}
            reps["personal"] = {field: getattr(representative, field) for field in personal_fields}
            reps["personal"]["gender"] = gender_dict[representative.gender]
            reps["personal"]["birth_date"] = representative.birth_date.strftime("%F") if representative.birth_date else None

            reps["contact"] = {}
            reps["contact"]["emails"] = [{"email": email.email, "type": email.kind} for email in representative.email_set.all()]
            reps["contact"]["websites"] = [{"website": website.url, "type": website.kind} for website in representative.website_set.all()]
            reps["contact"]["phones"] = [{"phone": phone.number, "type": phone.kind, "address": phone.address_id} for phone in representative.phone_set.all()]

            result.append(reps)

        print json.dumps(result, indent=4)
