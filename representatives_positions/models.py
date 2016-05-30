from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatewords
from taggit.managers import TaggableManager
from representatives.models import Representative


class Position(models.Model):
    representative = models.ForeignKey(Representative,
        related_name='positions')
    datetime = models.DateField()
    text = models.TextField()
    link = models.URLField()
    published = models.BooleanField(default=False)
    tags = TaggableManager()

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False

    def get_absolute_url(self):
        return reverse('representatives_positions:position-detail',
                args=(self.pk,))
