# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0007_auto_20150323_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='MGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Group')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('representatives.group',),
        ),
        migrations.CreateModel(
            name='MMandate',
            fields=[
                ('mandate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Mandate')),
                ('active', models.BooleanField(default=False)),
                ('mgroup', models.ForeignKey(to='legislature.MGroup')),
            ],
            options={
            },
            bases=('representatives.mandate',),
        ),
        migrations.CreateModel(
            name='MRepresentative',
            fields=[
                ('representative_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='representatives.Representative')),
                ('country', models.ForeignKey(to='representatives.Country', null=True)),
            ],
            options={
            },
            bases=('representatives.representative',),
        ),
        migrations.AddField(
            model_name='mmandate',
            name='mrepresentative',
            field=models.ForeignKey(to='legislature.MRepresentative'),
            preserve_default=True,
        ),
    ]
