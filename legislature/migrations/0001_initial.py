# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0004_representative_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('constituency_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Constituency')),
            ],
            options={
            },
            bases=('representatives.constituency',),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Group')),
            ],
            options={
            },
            bases=('representatives.group',),
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('mandate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Mandate')),
            ],
            options={
            },
            bases=('representatives.mandate',),
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('representative_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Representative')),
            ],
            options={
            },
            bases=('representatives.representative',),
        ),
    ]
