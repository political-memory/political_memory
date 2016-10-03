# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0007_auto_20151213_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituency',
            name='country',
            field=models.ForeignKey(blank=True, to='representatives.Country', null=True),
        ),
    ]
