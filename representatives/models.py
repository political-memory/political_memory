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


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.code)


class Representative(TimeStampedModel):
    """
    Base model for representatives
    """

    slug = models.SlugField(max_length=100)
    remote_id = models.CharField(max_length=255, unique=True)
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

    hashable_fields = ['remote_id']

    def __unicode__(self):
        return u'{} ({})'.format(smart_unicode(self.full_name), self.remote_id)

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


class Address(Contact):
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


class Phone(Contact):
    number = models.CharField(max_length=255, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')
    address = models.ForeignKey(Address, null=True, related_name='phones')


class Chamber(models.Model):
    """
    A representative chamber
    """
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', null=True, related_name='chambers')
    abbreviation = models.CharField(max_length=10, blank=True, default='',
        db_index=True)

    hashable_fields = ['name', 'country', 'abbreviation']

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.abbreviation)


class Group(TimeStampedModel):
    """
    An entity represented by a representative through a mandate
    """
    name = models.CharField(max_length=511, db_index=True)
    abbreviation = models.CharField(max_length=10, blank=True, default='',
        db_index=True)
    kind = models.CharField(max_length=255, db_index=True)
    chamber = models.ForeignKey(Chamber, null=True, related_name='groups')

    hashable_fields = ['name', 'abbreviation', 'kind', 'chamber']

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ('name',)


class Constituency(TimeStampedModel):
    """
    An authority for which a representative has a mandate
    """
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', null=True, blank=True,
        related_name='constituencies')

    hashable_fields = ['name', 'country']

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)


class MandateManager(models.Manager):
    """ This satisfies repr(Mandate) """
    def get_queryset(self):
        return super(
            MandateManager,
            self).get_queryset().select_related(
            'group',
            'constituency')


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

    hashable_fields = ['group', 'constituency', 'role', 'begin_date',
                       'end_date', 'representative']

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

    class Meta:
        ordering = ('-end_date',)
