# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0007_auto_20150323_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
