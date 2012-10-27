from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)


class Representative(models.Model):
    """
    FIXME
    """
    N_A = 0
    F = 1
    M = 2
    GENDER = (
        (N_A, "N/A"),
        (F, "F"),
        (M, "M"),
    )

    slug = models.SlugField(max_length=100)
    remote_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    gender = models.SmallIntergerField(choices=GENDER, default=N_A)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    cv = models.TextField(blank=True, null=True)


class Contact(models.Model):
    representative = models.ForeignKey(Representative)

    class Meta:
        abstract = True


class Email(Contact):
    email = models.EmailField()
    kind = models.CharField(max_length=255, blank=True, null=True)


class WebSite(Contact):
    url = models.URLField()
    kind = models.CharField(max_length=255, blank=True, null=True)


class Address(Contact):
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    floor = models.SmallIntergerField(blank=True, null=True)
    office_number = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # TODO Find standard for storage in charfield


class Phone(Contact):
    number = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address)


class Mandate(models.Model):
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, blank=True, null=True)
    short_id = models.CharField(max_length=25, blank=True, null=True)
    url = models.URLField()
    constituency = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Authority for which the mandate is realized. Eg.: a eurodeputies has a mandate at the European Parliament for a country"
    )
    role = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Eg.: president of a political group at the European Parliament"
    )
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # Sometimes begin_date and end_date are not available
    active = models.NullBooleanField(default=False)
