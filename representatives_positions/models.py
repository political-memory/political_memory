from django.db import models
from django.template.defaultfilters import truncatewords
from representatives.models import Representative


class Position(models.Model):
    representative = models.ForeignKey(Representative,
                                       related_name='positions')
    datetime = models.DateField()
    text = models.TextField()
    link = models.URLField(max_length=500)
    published = models.BooleanField(default=False)

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False
