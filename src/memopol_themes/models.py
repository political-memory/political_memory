from django.db import models
from django.utils.encoding import smart_unicode

from autoslug import AutoSlugField

from representatives.models import Representative
from representatives_votes.models import Dossier, Proposal
from representatives_positions.models import Position


class Theme(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()

    dossiers = models.ManyToManyField(Dossier, related_name='themes')
    proposals = models.ManyToManyField(Proposal, related_name='themes')
    positions = models.ManyToManyField(Position, related_name='themes')

    def __unicode__(self):
        return smart_unicode(self.name)


class ThemeLink(models.Model):
    title = models.CharField(max_length=511)
    datetime = models.DateField()
    link = models.URLField(max_length=500)
    theme = models.ForeignKey(Theme, related_name='links')

    def __unicode__(self):
        return smart_unicode('%s (%s)' % (self.title, self.link))


class ThemeScore(models.Model):
    representative = models.ForeignKey(Representative,
                                       related_name='themescores')
    theme = models.ForeignKey(Theme, related_name='themescores')
    score = models.FloatField(default=0)

    class Meta:
        managed = False
        ordering = ['theme__slug']
        db_table = 'memopol_themes_themescore'
