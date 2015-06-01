# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0010_auto_20150527_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandate',
            name='representative',
            field=models.ForeignKey(related_name='mandates', to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phone',
            name='address',
            field=models.ForeignKey(related_name='phones', to='representatives.Address', null=True),
            preserve_default=True,
        ),
    ]
