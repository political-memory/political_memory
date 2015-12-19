# coding: utf-8
from django.db import models
from django.template.defaultfilters import truncatewords
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from legislature.models import MemopolRepresentative


class PositionManager(models.Manager):
    """A simple model manager for querying published Positions"""
    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(published=True, **kwargs)


class Position(models.Model):
    representative = models.ForeignKey(
        MemopolRepresentative,
        related_name='positions')
    datetime = models.DateField()
    text = models.TextField()
    link = models.URLField()
    published = models.BooleanField(default=False)
    tags = TaggableManager()

    # Adds our custom manager
    objects = PositionManager()

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False

    def get_absolute_url(self):
        return reverse('positions:position-detail', args=(self.pk,))
