# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

import hashlib

from django.db import models
from django.utils.encoding import smart_str

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
                fingerprint.update(
                    getattr(self, field_name).fingerprint
                )
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
