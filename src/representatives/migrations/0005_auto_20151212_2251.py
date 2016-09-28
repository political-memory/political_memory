# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0004_auto_20150709_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandate',
            name='role',
            field=models.CharField(default=b'', help_text=b'Eg.: president of a political group', max_length=25, blank=True),
        ),
    ]
