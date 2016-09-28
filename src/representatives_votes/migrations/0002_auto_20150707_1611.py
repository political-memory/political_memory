# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150702_1827'),
        ('representatives_votes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='representative_remote_id',
        ),
        migrations.AddField(
            model_name='vote',
            name='representative',
            field=models.ForeignKey(
                related_name='votes',
                to='representatives.Representative',
                null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='representative_fingerprint',
            field=models.CharField(
                max_length=200,
                blank=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='representative_name',
            field=models.CharField(
                default='',
                max_length=200,
                blank=True),
            preserve_default=False,
        ),
    ]
