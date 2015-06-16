# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemopolGroup',
            fields=[
                ('group', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='representatives.Group')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('representatives.group',),
        ),
        migrations.CreateModel(
            name='MemopolRepresentative',
            fields=[
                ('representative_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Representative')),
                ('representative_remote_id', models.CharField(unique=True, max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('country', models.ForeignKey(to='representatives.Country', null=True)),
            ],
            options={
            },
            bases=('representatives.representative',),
        ),
    ]
