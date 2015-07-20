# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='datetime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='position',
            name='representative',
            field=models.ForeignKey(related_name='positions', to='legislature.MemopolRepresentative'),
        ),
    ]
