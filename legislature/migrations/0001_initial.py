# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150625_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemopolRepresentative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('representative', models.OneToOneField(parent_link=True, related_name='extra', null=True, on_delete=django.db.models.deletion.SET_NULL, to='representatives.Representative')),
                ('representative_remote_id', models.CharField(unique=True, max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('country', models.ForeignKey(to='representatives.Country', null=True)),
            ],
        ),
    ]
