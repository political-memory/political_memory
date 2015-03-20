from django.db import models
import representatives
import datetime


class Representative(representatives.models.Representative):
    active = models.BooleanField(default=False)
    country = models.ForeignKey(representatives.models.Country, null=True)

    def active_mandates(self):
        return self.mandate_set.filter(active=True)

    def former_mandates(self):
        return self.mandate_set.filter(active=False)

    def current_group(self):
        return self.mandate_set.get(
            active=True,
            group__kind='group'
        )

    def update_active(self):
        # If a representative has at least one active manadate
        self.active = False
        for mandate in self.mandate_set.all():
            if mandate.active:
                self.active = True
                continue

        self.save()

    def update_country(self):
        # Create a country if it does not exist
        # The representative's country is the one associated
        # with the last 'country' mandate
        country_mandate = self.mandate_set.filter(
            group__kind='country'
        ).order_by('-begin_date')[0:1].get()

        country, created = representatives.models.Country.objects.get_or_create(
            name=country_mandate.group.name,
            code=country_mandate.group.abbreviation
        )
        self.country = country
        self.save()


class Mandate(representatives.models.Mandate):

    def update_active(self):
        date = datetime.datetime.now().date()
        self.active = self.end_date > date
        self.save()
