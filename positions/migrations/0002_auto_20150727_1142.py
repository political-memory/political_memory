# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('positions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='dossier',
        ),
        migrations.AddField(
            model_name='position',
            name='tags',
            field=taggit.managers.TaggableManager(
                to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
