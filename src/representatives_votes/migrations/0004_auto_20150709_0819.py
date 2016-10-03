# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0003_auto_20150708_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposal',
            options={
                'ordering': ['datetime']},
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={
                'ordering': ['proposal__datetime']},
        ),
        migrations.AlterField(
            model_name='proposal',
            name='representatives',
            field=models.ManyToManyField(
                related_name='proposals',
                through='representatives_votes.Vote',
                to='representatives.Representative'),
        ),
    ]
