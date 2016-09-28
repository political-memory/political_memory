# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0013_constituency_country_related_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chamber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fingerprint', models.CharField(unique=True, max_length=40)),
                ('name', models.CharField(max_length=255)),
                ('country', models.ForeignKey(related_name='chambers', to='representatives.Country', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='chamber',
            field=models.ForeignKey(related_name='groups', to='representatives.Chamber', null=True),
        ),
    ]
