# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0012_index_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='country',
            field=models.ForeignKey(related_name='constituencies', blank=True, to='representatives.Country', null=True),
        ),
    ]
