# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0004_auto_20150709_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossier',
            name='reference',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
