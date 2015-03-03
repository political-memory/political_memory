# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemopolRepresentative',
            fields=[
                ('representative_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Representative')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('representatives.representative',),
        ),
    ]
