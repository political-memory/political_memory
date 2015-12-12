# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0003_auto_20150709_1601'),
        ('legislature', '0002_memopolrepresentative_main_mandate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateField()),
                ('text', models.TextField()),
                ('link', models.URLField()),
                ('published', models.BooleanField(default=False)),
                ('dossier', models.ForeignKey(blank=True,
                                              to='votes.MemopolDossier', null=True)),
                ('representative', models.ForeignKey(
                    related_name='positions', to='legislature.MemopolRepresentative')),
            ],
        ),
    ]
