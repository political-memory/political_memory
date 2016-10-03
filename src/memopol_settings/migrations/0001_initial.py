# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=255)),
                ('comment', models.TextField()),
            ],
        ),
    ]
