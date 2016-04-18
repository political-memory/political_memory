# coding: utf-8

import hashlib
from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str, smart_unicode
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


class HashableModel(models.Model):
    """
    An abstract base class model that provides a fingerprint
    field
    """

    fingerprint = models.CharField(
        max_length=40,
        unique=True,
    )

    class Meta:
        abstract = True

    def calculate_hash(self):
        fingerprint = hashlib.sha1()
        for field_name in self.hashable_fields:
            field = self._meta.get_field(field_name)
            if field.is_relation:
                related = getattr(self, field_name)
                if related is None:
                    fingerprint.update(smart_str(related))
                else:
                    fingerprint.update(related.fingerprint)
            else:
                fingerprint.update(
                    smart_str(getattr(self, field_name))
                )
        self.fingerprint = fingerprint.hexdigest()
        return self.fingerprint

    def get_hash_str(self):
        string = ''
        for field_name in self.hashable_fields:
            field = self._meta.get_field(field_name)
            if field.is_relation:
                string += getattr(self, field_name).fingerprint
            else:
                string += smart_str(getattr(self, field_name))
        return string

    def save(self, *args, **kwargs):
        self.calculate_hash()
        super(HashableModel, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2, unique=True)

    @property
    def fingerprint(self):
        fingerprint = hashlib.sha1()
        fingerprint.update(smart_str(self.name))
        fingerprint.update(smart_str(self.code))
        return fingerprint.hexdigest()

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.code)

    def get_absolute_url(self):
        return reverse('representatives:representative-list',
            kwargs=dict(group_kind='country', group=self.name))


class Representative(HashableModel, TimeStampedModel):
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

    def get_absolute_url(self):
        return reverse('representatives:representative-detail',
                args=(self.slug,))

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


class Chamber(HashableModel):
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


class Group(HashableModel, TimeStampedModel):
    """
    An entity represented by a representative through a mandate
    """
    name = models.CharField(max_length=255, db_index=True)
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

    def get_absolute_url(self):
        if self.chamber:
            return reverse('representatives:representative-list',
                kwargs=dict(group_kind=self.kind, chamber=self.chamber.name,
                    group=self.name))
        else:
            return reverse('representatives:representative-list',
                kwargs=dict(group_kind=self.kind, group=self.name))


class Constituency(HashableModel, TimeStampedModel):
    """
    An authority for which a representative has a mandate
    """
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', null=True, blank=True,
        related_name='constituencies')

    hashable_fields = ['name']

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


class Mandate(HashableModel, TimeStampedModel):

    objects = MandateManager()

    group = models.ForeignKey(Group, null=True, related_name='mandates')
    constituency = models.ForeignKey(
        Constituency, null=True, related_name='mandates')
    representative = models.ForeignKey(Representative, related_name='mandates')
    role = models.CharField(
        max_length=25,
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
