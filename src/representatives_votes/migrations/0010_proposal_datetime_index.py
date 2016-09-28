# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0009_dossier_ext_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='datetime',
            field=models.DateTimeField(db_index=True),
        ),
    ]
