# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='total_abstain',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='total_against',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='total_for',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
