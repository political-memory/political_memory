# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0018_auto_20160624_0517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamber',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='constituency',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='group',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='representative',
            name='fingerprint',
        ),
    ]
