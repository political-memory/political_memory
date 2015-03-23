# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0006_auto_20150320_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='email',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mandate',
            name='group',
            field=models.ForeignKey(to='representatives.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mandate',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phone',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='website',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
            preserve_default=True,
        ),
    ]
