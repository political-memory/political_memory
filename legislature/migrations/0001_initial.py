# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150702_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemopolRepresentative',
            fields=[
                ('representative_ptr', models.OneToOneField(parent_link=True, auto_created=True,
                                                            primary_key=True, serialize=False, to='representatives.Representative')),
                ('score', models.IntegerField(default=0)),
                ('country', models.ForeignKey(
                    to='representatives.Country', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('representatives.representative',),
        ),
    ]
