# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.code)


class Representative(models.Model):

    GENDER = (
        (0, "N/A"),
        (1, "F"),
        (2, "M"),
    )

    slug = models.SlugField(max_length=100)
    remote_id = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    gender = models.SmallIntegerField(choices=GENDER, default=0)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    cv = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=512, null=True)
    active =  models.BooleanField(default=False)

    def __unicode__(self):
        return self.full_name
    
    def gender_as_str(self):
        genders = {0: 'N/A', 1: 'F', 2: 'M'}
        return genders[self.gender]


# Contact related models
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
    floor = models.CharField(max_length=255, blank=True, null=True)
    office_number = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # TODO Find standard for storage in charfield


class Phone(Contact):
    number = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, null=True, related_name='phones')


# Mandate related models


class Group(models.Model):
    """
        An entity represented by a representative through a mandate
    """
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    kind = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)


class Constituency(models.Model):
    """
        An authority for which a representative has a mandate
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Mandate(models.Model):
    group = models.ForeignKey(Group, null=True)
    constituency = models.ForeignKey(Constituency, null=True)
    representative = models.ForeignKey(Representative, related_name='mandates')
    role = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Eg.: president of a political group at the European Parliament"
    )
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    link = models.URLField()

