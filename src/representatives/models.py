# coding: utf-8

from datetime import datetime

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.functional import cached_property


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Country(models.Model):
    objects = CountryManager()

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.code)

    def natural_key(self):
        return (self.code,)


class RepresentativeManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Representative(TimeStampedModel):
    """
    Base model for representatives
    """

    objects = RepresentativeManager()

    slug = models.SlugField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    full_name = models.CharField(max_length=255)
    GENDER = (
        (0, "N/A"),
        (1, "F"),
        (2, "M"),
    )
    gender = models.SmallIntegerField(choices=GENDER, default=0)
    birth_place = models.CharField(max_length=255, blank=True, default='')
    birth_date = models.DateField(blank=True, null=True)
    cv = models.TextField(blank=True, default='')
    photo = models.CharField(max_length=512, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_unicode(self.full_name)

    def natural_key(self):
        return (self.slug,)

    def gender_as_str(self):
        genders = {0: 'N/A', 1: 'F', 2: 'M'}
        return genders[self.gender]

    class Meta:
        ordering = ['last_name', 'first_name']

# Contact related models


class Contact(TimeStampedModel):
    representative = models.ForeignKey(Representative)

    class Meta:
        abstract = True


class Email(Contact):
    email = models.EmailField()
    kind = models.CharField(max_length=255, blank=True, default='')


class WebSite(Contact):
    url = models.CharField(max_length=2048, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')


class AddressManager(models.Manager):
    def get_by_natural_key(self, name, kind, representative_slug):
        representative = Representative.objects.get(slug=representative_slug)
        return self.get(name=name, kind=kind, representative=representative)


class Address(Contact):
    objects = AddressManager()

    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255, blank=True, default='')
    street = models.CharField(max_length=255, blank=True, default='')
    number = models.CharField(max_length=255, blank=True, default='')
    postcode = models.CharField(max_length=255, blank=True, default='')
    floor = models.CharField(max_length=255, blank=True, default='')
    office_number = models.CharField(max_length=255, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')

    def natural_key(self):
        representative_nk = self.representative.natural_key()
        return (self.name, self.kind) + representative_nk


class Phone(Contact):
    number = models.CharField(max_length=255, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')
    address = models.ForeignKey(Address, null=True, related_name='phones')


class ChamberManager(models.Manager):
    def get_by_natural_key(self, abbreviation):
        return self.get(abbreviation=abbreviation)


class Chamber(models.Model):
    """
    A representative chamber
    """
    objects = ChamberManager()

    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', null=True, related_name='chambers')
    abbreviation = models.CharField(max_length=10, blank=True, default='',
        db_index=True)

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.abbreviation)

    def natural_key(self):
        return (self.abbreviation,)


class GroupManager(models.Manager):
    def get_by_natural_key(self, name, kind, chamber_nk):
        if chamber_nk:
            chamber = Chamber.objects.get_by_natural_key(chamber_nk)
        else:
            chamber = None

        return self.get(name=name, kind=kind, chamber=chamber)


class Group(TimeStampedModel):
    """
    An entity represented by a representative through a mandate
    """
    objects = GroupManager()

    name = models.CharField(max_length=511, db_index=True)
    abbreviation = models.CharField(max_length=10, blank=True, default='',
        db_index=True)
    kind = models.CharField(max_length=255, db_index=True)
    chamber = models.ForeignKey(Chamber, null=True, related_name='groups')

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        chamber_nk = self.chamber.natural_key() if self.chamber else (None,)
        return (self.name, self.kind) + chamber_nk

    class Meta:
        ordering = ('name',)


class ConstituencyManager(models.Manager):
    def get_by_natural_key(self, name, country_nk):
        if country_nk:
            country = Country.objects.get_by_natural_key(country_nk)
        else:
            country = None

        return self.get(name=name, country=country)


class Constituency(TimeStampedModel):
    """
    An authority for which a representative has a mandate
    """
    objects = ConstituencyManager()

    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', null=True, blank=True,
        related_name='constituencies')

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        country_nk = self.country.natural_key() if self.country else (None,)
        return (self.name,) + country_nk


class MandateManager(models.Manager):
    """ This satisfies repr(Mandate) """
    def get_queryset(self):
        return super(
            MandateManager,
            self).get_queryset().select_related(
            'group',
            'constituency')

    def get_by_natural_key(self, begin_date, end_date, representative_slug,
                           group_name, group_kind, group_chamber_nk):
        representative = Representative.objects.get_by_natural_key(
            representative_slug)
        group = Group.objects.get_by_natural_key(group_name, group_kind,
                                                 group_chamber_nk)
        return self.get(begin_date=begin_date, end_date=end_date,
                        representative=representative, group=group)


class Mandate(TimeStampedModel):
    objects = MandateManager()

    group = models.ForeignKey(Group, null=True, related_name='mandates')
    constituency = models.ForeignKey(
        Constituency, null=True, related_name='mandates')
    representative = models.ForeignKey(Representative, related_name='mandates')
    role = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Eg.: president of a political group"
    )
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    link = models.URLField()

    @property
    def active(self):
        return self.end_date >= datetime.now().date()

    def __unicode__(self):
        t = u'Mandate : {representative},{role} {group} for {constituency}'
        return t.format(
            representative=self.representative,
            role=(
                u' {} of'.format(
                    self.role) if self.role else u''),
            constituency=self.constituency,
            group=self.group)

    def natural_key(self):
        rep_nk = self.representative.natural_key() \
            if self.representative else (None,)
        group_nk = self.group.natural_key() \
            if self.group else (None, None, None)

        return (self.begin_date, self.end_date) + rep_nk + group_nk

    class Meta:
        ordering = ('-end_date',)
