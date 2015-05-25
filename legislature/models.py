from django.db import models
import representatives
import datetime


class MRepresentative(representatives.models.Representative):
    # active = models.BooleanField(default=False)
    country = models.ForeignKey(representatives.models.Country, null=True)

    def active_mandates(self):
        return self.mmandate_set.filter(active=True)

    def former_mandates(self):
        return self.mmandate_set.filter(active=False)

    def current_group_mandate(self):
        return self.mmandate_set.get(
            active=True,
            group__kind='group'
        )

    def update_active(self):
        # If a representative has at least one active manadate
        self.active = False
        for mandate in self.mmandate_set.all():
            if mandate.active:
                self.active = True
                break

        self.save()

    def update_country(self):
        # Create a country if it does not exist
        # The representative's country is the one associated
        # with the last 'country' mandate
        country_mandate = self.mmandate_set.filter(
            group__kind='country'
        ).order_by('-begin_date')[0:1].get()

        country, created = representatives.models.Country.objects.get_or_create(
            name=country_mandate.group.name,
            code=country_mandate.group.abbreviation
        )
        self.country = country
        self.save()


class MGroup(representatives.models.Group):
    active = models.BooleanField(default=False)

    def update_active(self):
        self.active = False
        for mandate in self.mmandate_set.all():
            if mandate.active:
                self.active = True
                break
        self.save()


class MMandate(representatives.models.Mandate):
    active = models.BooleanField(default=False)
    mgroup = models.ForeignKey(MGroup)
    mrepresentative = models.ForeignKey(MRepresentative)

    def update_active(self):
        date = datetime.datetime.now().date()
        self.active = self.end_date > date
        self.save()
